import asyncio
import aiohttp
import openpyxl
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from api.models import Article, File
from api.serializers import FileSerializer, ArticleSerializer


class ArticleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API принимающее один артикул"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = serializer.validated_data['article']
        dct = {}
        async def main():
            async with aiohttp.ClientSession() as session:
                url = f'https://card.wb.ru/cards/detail?nm={str(article)}'
                async with session.get(url) as resp:
                    data = await resp.json(content_type=None)
                    if data['data']['products']:
                        dct['article'] = data['data']['products'][0]['id']
                        dct['brand'] = data['data']['products'][0]['brand']
                        dct['title'] = data['data']['products'][0]['name']

        asyncio.run(main())
        if dct:
            return Response(dct)
        else:
            return Response(f'Товар c артикулом {article} не найден')


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
                            article = data['data']['products'][0]['id']
                            brand = data['data']['products'][0]['brand']
                            title = data['data']['products'][0]['name']
                            dct = {'article': article, 'brand': brand, 'title': title}
                            goods.append(dct)

        asyncio.run(main())
        return Response(goods)
