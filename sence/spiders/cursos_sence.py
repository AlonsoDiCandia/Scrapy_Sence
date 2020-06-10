# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from sence.items import SenceItem
import re

class CursosSenceSpider(scrapy.Spider):
	name = 'cursos_sence'
	allowed_domains = ['eligemejor.sence.cl']
	start_urls = ['https://eligemejor.sence.cl/BuscarCursoNuevo/Buscar']

	headers = {
	"authority": "eligemejor.sence.cl",
	"pragma": "no-cache",
	"cache-control": "no-cache",
	"upgrade-insecure-requests": "1",
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125",
	"origin": "https://eligemejor.sence.cl",
	"content-type": "application/x-www-form-urlencoded",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"sec-fetch-site": "same-origin",
	"sec-fetch-mode": "navigate",
	"sec-fetch-user": "?1",
	"sec-fetch-dest": "document",
	"referer": "https://eligemejor.sence.cl/BuscarCursoNuevo/Buscar",
	"accept-language": "es-419,es;q=0.9"
	}

	cookies = {"ASP.NET_SessionId":"kyvpbxufnujkudq1pjyxdygv",
		"_ga":"GA1.2.1459653529.1591667712",
		".ASPXAUTH":"E6FF3D7271E3D98506E478365F1591F370EF21B51819FA5DF0A48B225A6B51DA5F48067409AF0BF952E7D48FC8A8A0DB438467293A518C855E55BFB611C21F5B6727"
	}

	def start_requests(self):
		yield Request(
				url=self.start_urls[0],
				headers=self.headers,
				cookies=self.cookies,
				callback=self.parse,
				method='POST',
				body=self.create_body(str(1)),
				dont_filter=True
				)

	def parse(self, response):

		course_name = response.xpath('//h4[@class="cursoTitulo movitit"]/b').extract()
		for name in course_name:
			name = name.replace('<b>', '').replace('</b>', '')
			item = SenceItem()
			item['course_name'] = name
			yield item

		try:
			new_page = response.xpath('//div[@class="pagination-container"]/ul/li[@class="PagedList-skipToNext"]').re('Pagina\([\d]+\)')[0]
			if new_page:
				number_page = re.search(r'[\d]+', new_page).group()
			yield Request(
					url = self.start_urls[0],
					headers=self.headers,
					cookies=self.cookies,
					callback=self.parse,
					method='POST',
					body=self.create_body(number_page),
					dont_filter=True
				)
		except:
			print("No more pages.")

	def create_body(self, number_page):
		return 'Buscador=&OrdenarPor=2&Orden=Ascendente&Pagina=' + number_page +'&ResultadosPorPagina=10&BuscarConFiltro=1&ParticipantesTramo1=0&ParticipantesTramo2=0&ParticipantesTramo3=0&\
				ComiteParitario=False&Tipo=Curso&OpcionTipo=2&OpcionTipoOtec=2&Region=&RutOtec=0&DvOtec=&OrigenLlamada=&AplicoFiltro=0&FiltroNombreCurso=&\
				filtro_check_NombreProgramaSinTipo_Cursos+En+L%C3%ADnea_Equals=on&filtro_check_Modalidad_E-Learning_Equals=on&filtro_check_AreaCurso_Administraci%C3%B3n_Equals=on&\
				filtro_check_AreaCurso_Comercio_Equals=on&filtro_check_AreaCurso_Computaci%C3%B3n+E+Inform%C3%A1tica_Equals=on&filtro_check_AreaCurso_Gastronom%C3%ADa+Hoteler%C3%ADa+Y+Turismo_Equals=on&\
				filtro_check_AreaCurso_Idiomas+Y+Comunicaci%C3%B3n_Equals=on&filtro_check_AreaCurso_Transversales_Equals=on&filtro_check_NombreRegion_Todas_Equals=on&\
				filtro_check_NombreComunaSinRegion_Todas_Equals=on&filtro_rangoFecha_FechaInicioCurso=&filtro_rangoFecha_FechaInicioCurso=&filtro_rangoFecha_FechaInicioCurso=0%2C0&filtro_slider_PondCursoInt=0%2C6'

