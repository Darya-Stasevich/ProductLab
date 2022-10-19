import asyncio
import json

import aiohttp
import openpyxl
from django.http import JsonResponse, HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser
from api.models import Article, File
from api.serializers import FileSerializer, ArticleSerializer
from pydantic import BaseModel, ValidationError


class Item(BaseModel):
    article: int
    brand: str
    title: str


class ArticleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API принимающее один артикул"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = serializer.validated_data['article']
        self.perform_create(serializer)
        async def main():
            async with aiohttp.ClientSession() as session:
                url = f'https://card.wb.ru/cards/detail?nm={str(article)}'
                async with session.get(url) as resp:
                    data = await resp.json(content_type=None)
                    if data['data']['products']:
                        art = data['data']['products'][0]['id']
                        brand = data['data']['products'][0]['brand']
                        title = data['data']['products'][0]['name']
                        try:
                            item = Item(article=art, brand=brand, title=title)
                            return(item.dict())
                        except ValidationError as e:
                            e.json()
                            return('Invalid data')
                    else:
                        return (f'Article {article} was not found')

        res = asyncio.run(main())
        return HttpResponse(json.dumps(res, ensure_ascii=False))


class FileUploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API принимающее файл формата xlsx"""
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FileUploadParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        self.perform_create(serializer)
        book = openpyxl.open(file, read_only=True)
        sheet = book.active
        goods = []

        async def main():
            async with aiohttp.ClientSession() as session:
                for row in range(1, sheet.max_row + 1):
                    url = f'https://card.wb.ru/cards/detail?nm={str(sheet[row][0].value)}'
                    async with session.get(url) as resp:
                        data = await resp.json(content_type=None)
                        if data['data']['products']:
                            art = data['data']['products'][0]['id']
                            brand = data['data']['products'][0]['brand']
                            title = (data['data']['products'][0]['name'])
                            try:
                                item = Item(article=art, brand=brand, title=title)
                                goods.append(item.dict())
                            except ValidationError as e:
                                e.json()

        asyncio.run(main())
        if goods:
            return HttpResponse(json.dumps(goods, ensure_ascii=False))
        else:
            return JsonResponse('Goods are not found', safe=False)
