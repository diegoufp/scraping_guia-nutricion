import scrapy 
class VerduraSpider(scrapy.Spider):
    name = "basic"
    start_urls = ['http://www.guia-nutricion.com/']
    custom_settings = {
        'FEEDS':{
        'nutrientes.json':{
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'indent': 0
            #,
            #'item_export_kwargs': {
                 #'export_empty_fields': True,
                }
            }
        }

    def parse(self, response):
        links_principal = response.xpath('//div[@class="col-lg-8 col-md-9"]/div[@class="row"]//a/@href').getall()
        for link in links_principal:
            yield response.follow(link, callback=self.productos_parse,  cb_kwargs={'url': response.urljoin(link)})

    def productos_parse(self,response,**kwargs):
        # si existe una lista con links
        if response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']/a"):
            productos = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']/a[@class='list-group-item']/@href").getall()
            for producto in productos:
                yield response.follow(producto, callback=self.sublink, cb_kwargs={'url': response.urljoin(producto)})

            #next
            if response.xpath("//ul[@class='pagination']"):
                indice = response.xpath("//ul[@class='pagination']//a/text()").getall()
                if str(indice[-1]) == "»":
                    link_indice = response.xpath("//ul[@class='pagination']//a/@href").getall()
                    yield response.follow(link_indice[-1], callback=self.productos_parse, cb_kwargs={'url': response.urljoin(link_indice[-1])})

    def sublink(self,response,**kwargs):
        # extrayendo la informacion de los nutrientes
        if response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']"):
            s = []
            r = {}
            titulo = str(response.xpath("//h1/text()").get())
            lista_nutrientes = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom']").getall()
            for n in range(1,int(len(lista_nutrientes)) + 1):
                if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//div[@class='col-md-4 col-xs-12']"):
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-xlg inner-top-sm inner-bottom-xs border-bottom']/text()").get()).rstrip().lstrip()  })
                    # sub_nutrientes
                    if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]'):
                        sub_nutrientes = response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]').getall()
                        if int(len(sub_nutrientes)) == 1:
                            if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]'):
                                s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                            else:
                                 s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                        elif int(len(sub_nutrientes)) > 1:
                            for z in range(1,int(len(sub_nutrientes)) + 1):
                                if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h4 text-default"]'):
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                                else:
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                else: 
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
                    # sub_nutrientes
                    if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]'):
                        sub_nutrientes = response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]').getall()
                        if int(len(sub_nutrientes)) == 1:
                            if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]'):
                                s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                            else:
                                 s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                        elif int(len(sub_nutrientes)) > 1:
                            for z in range(1,int(len(sub_nutrientes)) + 1):
                                if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h4 text-default"]'):
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                                else:
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})
            
            # buscar la proteina
            otros = response.xpath('//div[@class="col-md-6 col-xs-12"]').getall()
            for x in range(1,int(len(otros)) + 1):
                if str(response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get()) == ("Proteina" or "proteina"):
                    if response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h4 text-default"]'):
                        s.append( { str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get() ).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                    else: 
                        s.append( { str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get() ).rstrip().lstrip() : "0" } )
            # ordenar el diccionario
            for t in s:
                r.update(t)

            # buscando los links del nav
            nav = response.xpath("//ul[@class='nav nav-tabs nav-justified']//a/@href").getall()
            yield response.follow(nav[1], callback=self.vitaminas, cb_kwargs={ titulo.rstrip().lstrip(): r})    

            #verifica si hay sublinks en los productos
            if response.xpath("//div[@class='row inner-bottom-xs']//div[@class='dropdown']"):
                sublinks = response.xpath("//div[@class='row inner-bottom-xs']//div[@class='dropdown']//a/@href").getall()
                for sub in sublinks:
                    yield response.follow(sub,callback=self.nutrientes, cb_kwargs={'url':  response.urljoin(sub)})

    def nutrientes(self,response,**kwargs):
        if response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']"):
            s = []
            r = {}
            titulo = str(response.xpath("//h1/text()").get())
            # buscar la mayoria de los nutrienes
            lista_nutrientes = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom']").getall()
            for n in range(1,int(len(lista_nutrientes)) + 1):
                if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//div[@class='col-md-4 col-xs-12']"):
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-xlg inner-top-sm inner-bottom-xs border-bottom']/text()").get()).rstrip().lstrip()  })
                    # sub_nutrientes
                    if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]'):
                        sub_nutrientes = response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]').getall()
                        if int(len(sub_nutrientes)) == 1:
                            if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]'):
                                s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                            else:
                                 s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                        elif int(len(sub_nutrientes)) > 1:
                            for z in range(1,int(len(sub_nutrientes)) + 1):
                                if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h4 text-default"]'):
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                                else:
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                else: 
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
                    # sub_nutrientes
                    if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]'):
                        sub_nutrientes = response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]').getall()
                        if int(len(sub_nutrientes)) == 1:
                            if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]'):
                                s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                            else:
                                 s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

                        elif int(len(sub_nutrientes)) > 1:
                            for z in range(1,int(len(sub_nutrientes)) + 1):
                                if response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h4 text-default"]'):
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                                else:
                                    s.append( { str( response.xpath(f'//div[@class="col-lg-8 col-md-9 contenidoLeft"]//div[@class="row border-bottom"][{n}]//div[@class="col-md-8 col-xs-12"]/div[@class="panel panel-default"][{z}]//p[@class="h3 text-primary reset-margin"]/text()').get()).rstrip().lstrip() : "0"})

            # buscar la proteina
            otros = response.xpath('//div[@class="col-md-6 col-xs-12"]').getall()
            for x in range(1,int(len(otros)) + 1):
                if str(response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get()) == ("Proteina" or "proteina"):
                    if response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h4 text-default"]'):
                        s.append( { str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get() ).rstrip().lstrip() : str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h4 text-default"]/text()').get()).rstrip().lstrip() } )
                    else: 
                        s.append( { str( response.xpath(f'//div[@class="col-md-6 col-xs-12"][{x}]//p[@class="h3 text-primary reset-margin"]/text()').get() ).rstrip().lstrip() : "0" } )
            # ordenar el diccionario
            for t in s:
                r.update(t)

            # buscando los links del nav
            nav = response.xpath("//ul[@class='nav nav-tabs nav-justified']//a/@href").getall()
            yield response.follow(nav[1], callback=self.vitaminas, cb_kwargs={ titulo.rstrip().lstrip(): r})    

    def vitaminas(self,response,**kwargs):
        s = []
        for z in kwargs.items():
            titulo = z[0]
            dicc = z[1]
        if response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']"):
            # lista de vitaminas
            lista_vitaminas = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom']").getall()
            for n in range(1,int(len(lista_vitaminas)) + 1):
                if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//div[@class='col-md-4 col-xs-12']"):
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-xlg inner-top-sm inner-bottom-xs border-bottom']/text()").get()).rstrip().lstrip()  })
                    

                else: 
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
            # ordenar el diccionario
            for t in s:
                dicc.update(t)
            # buscando los links del nav
            nav = response.xpath("//ul[@class='nav nav-tabs nav-justified']//a/@href").getall()
            yield response.follow(nav[2], callback=self.minerales, cb_kwargs={ titulo: dicc})   
                    
    def minerales(self,response,**kwargs):
        s = []
        for z in kwargs.items():
            titulo = z[0]
            dicc = z[1]
        if response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']"):
            # lista de vitaminas
            lista_minerales = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom']").getall()
            for n in range(1,int(len(lista_minerales)) + 1):
                if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//div[@class='col-md-4 col-xs-12']"):
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-xlg inner-top-sm inner-bottom-xs border-bottom']/text()").get()).rstrip().lstrip()  })
                    

                else: 
                    s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
            # ordenar el diccionario
            for t in s:
                dicc.update(t)
            # buscando los links del nav
            nav = response.xpath("//ul[@class='nav nav-tabs nav-justified']//a/@href").getall()
            yield response.follow(nav[4], callback=self.grasas, cb_kwargs={ titulo: dicc})
    
    def grasas(self,response,**kwargs):
        s = []
        for z in kwargs.items():
            titulo = z[0]
            dicc = z[1]
        if response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']"):
            lista_grasas = response.xpath("//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='panel-body']/div[@class='row border-bottom']").getall()
            for n in range(1,int(len(lista_grasas)) + 1):
                if str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='panel-body']/div[@class='row border-bottom'][{n}]//h2/text()").get()) == "Grasas Saturadas":
                    if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//div[@class='col-md-4 col-xs-12']"):
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-xlg inner-top-sm inner-bottom-xs border-bottom']/text()").get()).rstrip().lstrip()  })
                    
                    else: 
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
                elif str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='panel-body']/div[@class='row border-bottom'][{n}]//h2/text()").get()) == "Ácidos grasos monoinsaturados":
                    if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-md inner-top-sm inner-bottom-xs']"):
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-md inner-top-sm inner-bottom-xs']/text()").get()).rstrip().lstrip()  })
                    else: 
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })
                elif str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='panel-body']/div[@class='row border-bottom'][{n}]//h2/text()").get()) == "Ácidos grasos poliinsaturados":
                    if response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-md inner-top-sm inner-bottom-xs']"):
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//p[@class='text-md inner-top-sm inner-bottom-xs']/text()").get()).rstrip().lstrip()  })
                    else: 
                        s.append( { str(response.xpath(f"//div[@class='col-lg-8 col-md-9 contenidoLeft']//div[@class='row border-bottom'][{n}]//h2/text()").get()).rstrip().lstrip() : "0" })

            # ordenar el diccionario
            for t in s:
                dicc.update(t)
            yield {
                titulo: dicc
            }
                    

   
