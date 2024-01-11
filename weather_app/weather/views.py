from typing import Any

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request

import requests

from weather.filters.weather import WeatherFilter
from weather.models import Coordinate
from weather.serializers.weather import WeatherSerializer
from weather.services.fuzzy_service import FuzzyService
from weather.services.redis import RedisService
from weather_app import settings


class WeatherView(ListAPIView):

    serializer_class = WeatherSerializer
    filterset_class = WeatherFilter
    queryset = Coordinate.objects.order_by('name')

    URL = 'https://api.weather.yandex.ru/v2/informers?lat={}&lon={}'
    EX = 60 * 30  # 30 minutes

    @extend_schema(
        methods=['GET'],
        description="Погода по названию города",
        parameters=[
            OpenApiParameter(
                name='username',
                description='Имя пользователя для ограничения на запросы',
                required=True,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses=WeatherSerializer
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # Query parameter name is required
        if not request.query_params.get('city'):
            return Response('Parameter "name" is required!')

        queryset = self.filter_queryset(self.queryset)

        if not queryset.exists():
            # Get most similar city by algorithm Levenshtein (fuzzywuzzy)
            city: Coordinate | None = self.__get_most_similar_city(request.query_params.get('city'))
        else:
            city: Coordinate = queryset.first()

        if city is None:
            return Response('Город не найден', status=404)
        redis = RedisService()

        # Return cached data if it exists (EX time)
        if cached_data := redis.get(f"{request.query_params.get('username')}-{city.name}"):
            return Response(cached_data)

        # Get data from Yandex API
        response: requests.Response = self.get_weather_data_from_yandex(city)
        response_data: dict = response.json()

        try:
            serializer = self.serializer_class(response_data['fact'])
            data: str = self.__handle_yandex_api_data(city=city.name, serializer_data=serializer.data)

        except KeyError:
            return Response(f'Error - {response.text}')

        # Caching data for EX time
        redis.set(
            f"{request.query_params.get('username')}-{city.name}",
            data,
            ex=self.EX
        )

        return Response(data)

    def get_weather_data_from_yandex(self, city: Coordinate) -> requests.Response:
        url: str = self.URL.format(city.latitude, city.longitude)

        headers = {"X-Yandex-API-Key": settings.WEATHER_API_TOKEN}
        response: requests.Response = requests.get(url, headers=headers)
        return response

    def __get_most_similar_city(self, name: str) -> Coordinate | None:
        cities: list[str] = self.queryset.values_list('name', flat=True)
        most_similar_city: str = FuzzyService.get_most_similar(cities, name)

        answer: Coordinate | None = self.queryset.filter(name=most_similar_city).first()
        return answer

    def __handle_yandex_api_data(self, city: str, serializer_data: dict) -> str:
        return (
            f'Город: <b>{city}</b>\n\n'
            f'Температура: <b>{serializer_data["temp"]}°C</b>\n'
            f'Скорость ветра: <b>{serializer_data["wind_speed"]} м/с</b>\n'
            f'Давление: <b>{serializer_data["pressure_mm"]} мм рт. ст.</b>\n'
        )

