import pymysql

from datetime import date, timedelta
import datetime
from Misc.functions import *
import traceback
class Setting:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="root", database="carintocash_api", charset='utf8mb4')
    def read(self, id):
        con = Setting.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM setting")
            else:
                cursor.execute("SELECT * FROM setting where id = %s ", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    def update(self, id, data):
        con = Setting.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE setting set p1 = %s, p2 = %s, p3 = %s , p4 = %s , p5 = %s,  p6 = %s ,  p1_min = %s,  p1_max = %s,  p2_min = %s,  p2_max = %s,  p3_min = %s,  p3_max = %s,  p4_min = %s,  p4_max = %s,  p5_min = %s,  p5_max = %s,  p6_max = %s where id = %s",
                           (data['p1'], data['p2'], data['p3'], data['p4'], data['p5'],data['p6'],data['p1_min'],data['p1_max'],data['p2_min'],data['p2_max'],data['p3_min'],data['p3_max'],data['p4_min'],data['p4_max'],data['p5_min'],data['p5_max'],data['p6_max'], id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    def getyears(self, id):
        con = Setting.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT year FROM years order by year DESC")
            else:
                cursor.execute("SELECT * FROM setting where id = %s ", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def getmakes(self, data):
        con = Setting.connect(self)
        cursor = con.cursor()
        try:           
            cursor.execute("SELECT m.id makeId, m.name make, m.shortcode makecode FROM makes m LEFT Join vehiclespecschema_year vssy ON m.id = vssy.make_id Where vssy.year = %s" , (data['year'],) )           
            return cursor.fetchall()           
        except:
            return ()
        finally:
            con.close()
    def getmodels(self, data):
        con = Setting.connect(self)
        cursor = con.cursor()
        try:           
            cursor.execute("SELECT m.id makeId, m.name make, md.name model, md.id modelId FROM makes m LEFT Join vehiclespecschema_year vssy ON m.id = vssy.make_id LEFT JOIN vehiclespecschema_model vssm ON vssm.vssy_id = vssy.id LEFT JOIN models md ON md.id = vssm.modelId  Where vssy.year = %s AND m.id = %s ", (data['year'], data['make'],))
            return cursor.fetchall()           
        except:
            return ()
        finally:
            con.close()

    def getKip(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        current_time = datetime.datetime.now()
        current_time1 = current_time.strftime("%Y-%m-%d")

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT count(DATE_FORMAT(`created_at`, '%Y-%m-%d')) FROM `accepted_aps` WHERE DATE_FORMAT(`created_at`, '%Y-%m-%d') = CURDATE()")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()


    def getKipWeek(self):
        con = Setting.connect(self)
        cursor = con.cursor()

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("select COUNT(*) from `accepted_aps` where week(`created_at`) = week(now())")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()


    def getKipMonth(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("select COUNT(*) from `accepted_aps` where MONTH(`created_at`) = MONTH(now()) and YEAR(`created_at`) = YEAR(now())")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()
            
    def getCompleteInquiry(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT count(*) FROM accepted_aps where status = %s ", ('complete',))
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()


    def getInCompleteInquiry(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT count(*) FROM accepted_aps where status = %s ", ('incomplete',))
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()
            
    def getAcceptInquiry(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT count(*) FROM accepted_aps where status = %s ", ('accept',))
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()
            
    def userComesFrom(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT ref_id, COUNT(ref_id) FROM `accepted_aps` WHERE `ref_id` !='' GROUP BY ref_id")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()
            
            
    def userComesFromAll(self):
        con = Setting.connect(self)
        cursor = con.cursor()
        

        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT COUNT(ref_id) FROM `accepted_aps` WHERE `ref_id` !='' ")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close() 

    def getTranslateTxt(self,lang):

        if lang=='es':
            inAuctionstatus =  [{'Home' : 'Hogar','How_it_Works':'Cómo funciona','Faqs':'Preguntas Frecuentes','About_Us':'Acerca de Nosotros','Contact_Us':'Contáctenos','header_btn_txt':'Obtén una oferta instantánea por tu coche ahora'
            ,'sidebar_heading':'Obtén una Oferta Instantánea','sidebar_description':"Llevaremos un registro de tus respuestas aquí. Puedes volver a una pregunta anterior en cualquier momento."
            ,'sidebar_question1':'Acerca de tu coche'
            ,'sidebar_question2':'Ubicación'
            ,'sidebar_question3':'Kilometraje'
            ,'sidebar_question4':"Daño corporal"
            ,'sidebar_question5':"bolsas de aire"
            ,'sidebar_question6':"Arranca y conduce"
            ,'sidebar_question7':"Problemas mecánicos"
            ,'sidebar_question8':"Llaves"
            ,'sidebar_question9':"Tipo de Título"
            ,'sidebar_question10':"Daños por agua o fuego"
            ,'sidebar_question11':"Ofrece una cantidad"
            ,'sidebar_question12':"Aceptar"
            ,'sidebar_question13':"ubicación actual"
            ,'sidebar_question14':"Seu nome e telefone"
            ,'sidebar_question15':"nombre del propietario"
            ,'sidebar_question16':"nombre del beneficiario"
            ,'step_question1':"Cuéntanos un poco acerca de tu coche"
            ,'year_label':"Año"
            ,'make_label':"Hacer"
            ,'model_label':"Modelo"
            ,'Autofill_with_VIN':"Relleno automático con VIN"
            ,'title_vin':"¿Cuál es el número de identificación del vehículo de tu coche?"
            ,'subtitle_vin':"Usando tu  VIN, podemos identificar rápidamente el año, marca, modelo y versión de tu automóvil."
            ,'back':"Atrás"
            ,'autofill':"Autocompletar"
            ,'where_is_your':"Donde Esta tu"
            ,'located':"ubicado?"
            ,'zip_subtitle1':"Ingrese el código postal donde se encuentra su"
            ,'zip_subtitle2':"Estará estacionado cuando vengamos a buscarlo. (Esta información nos ayuda a determinar el monto de la oferta)."
            ,'Enter_vehicle_location':"Ingrese la ubicación del vehículo"
            ,'ZIP_code':"Código postal"
            ,'mileage_title':"¿Cuál es el kilometraje que muestra el odómetro?"
            ,'mileage_subtitle':"Si no sabe el número exacto, está bien, siempre que esté dentro de las 1000 millas, lo aceptaremos."
            ,'Mileage_on_odometer':"Kilometraje en el odómetro"
            ,'Unable_to_verify':"No se puede verificar"
            ,'next':"Próxima"
            ,'Does_your':"¿Tiene tu"
            ,'damage_title':"¿Tiene daños en la carrocería u óxido?"
            ,'damage_subtitle':"El daño/óxido de la carrocería se refiere a imperfecciones exteriores más grandes que el puño."
            ,'damage_question1':"¡No, mi vehículo está en buenas condiciones!"
            ,'damage_question2':"Sí, mi vehículo tiene algún daño u óxido."
            ,'drive_title1':"¿Puedes arrancar y conducir tu"
            ,'drive_subtitle1':"Esto nos habla de su"
            ,'drive_subtitle2':"condición y también nos ayuda a determinar cuál es la mejor grúa para usar en la recogida. Si funciona y se conduce, nuestro conductor de remolque debe poder conducirlo cuando lo recoja."
            ,'mechanical_title1':"¿Tiene algún problema mecánico?"
            ,'mechanical_subtitle1':"¡Compraremos tu coche pase lo que pase! Esto simplemente nos ayuda a determinar cómo se manejará su vehículo."
            ,'title_title1':"¿Tienes un título limpio?"
            ,'title_subtitle1':"Cada estado es diferente, pero si alguna vez una compañía de seguros declaró pérdida total a su vehículo, entonces podría tener un título de salvamento."
            ,'firedamage_title1':"Tiene su"
            ,'firedamage_title2':"¿Alguna vez ha tenido daños por agua o fuego?"
            ,'firedamage_subtitle1':"Los daños por agua e incendio pueden ser poco frecuentes; utilizamos esta información para ayudarnos a determinar el mejor uso de su vehículo."
            ,'Your':"Su"
            ,'offer_title1':"¡Es exactamente lo que necesitamos!"
            ,'offer_title2':"Nosotras te pagaremos"
            ,'Sell_instantly':"Vender al instante"
            ,'Decline':"Rechazar"
            ,'offer_title3':"Acepto la oferta. ¡Iremos a recoger su vehículo GRATIS y le pagaremos en el acto!"
            ,'start_from_begining':"Empezar desde el principio"
            ,'accept_title1':"¿Dónde deberíamos recoger tu"
            ,'Residence':"Residencia"
            ,'Business':"Negocio"
            ,'Location_Name':"Nombre del lugar"
            ,'Street_name':"Nombre de la calle*"
            ,'Address_line_2':"Línea de dirección 2"
            ,'City':"Ciudad*"
            ,'Select_a_state':"Selecciona un Estado*"
            ,'What_is_your_name_and_phone_number':"¿Cuál es tu nombre y número de teléfono?"
            ,'Full_Name':"Nombre completo*"
            ,'Phone':"Teléfono*"
            ,'Alternate_Phone':"Teléfono alternativo"
            ,'owner_title1':"¿Cuál es el nombre del propietario que aparece en el título?"
            ,'owner_subtitle1':"Enumere todos los nombres en el título."
            ,'USE_MY_NAME':"USA MI NOMBRE"
            ,'Full_Name_on_the_title':"Nombre completo en el título"
            ,'getting_paid':"¿A quién le pagan?"
            ,'Payee_Full_name':"Nombre completo del beneficiario"
            ,'You_are_all_finished':"¡Estáis todos acabados!"
            ,'reaching':"¡Alguien se comunicará pronto!"
            ,'Have_another_car_to_sell':"¿Tiene otro auto para vender?"
            ,'Select_where_your':"Seleccione donde su"
            ,'has_rust_or_body_damage':"tiene óxido o daños en la carrocería"
            ,'airbag_title1':"¿Su automóvil tiene actualmente algún airbag desplegado?"
            ,'airbag_subtitle1':"Especifique si su vehículo tiene actualmente las bolsas de aire desplegadas, esto incluye daños interiores previos."
            ,'key_title1':"¿Tienes llaves para tu"
            ,'key_subtitle1':"Esto nos ayuda a saber qué esperar cuando vayamos a recoger su vehículo."
            ,'Calculating':"Calculadora..."
            ,'Decline_offer':"Rechazar una oferta"
            ,'Name':"Nombre*"
            ,'Enter_name':"Ingrese su nombre*"
            ,'Email':"Correo electrónico*"
            ,'Enter_email':"Ingrese correo electrónico*"
            ,'Phone_Number':"Número de teléfono*"
            ,'Enter_phone_number':"Ingresa número telefónico*"
            ,'decline_question1':"¿Cuánto aceptarías por tu vehículo?*"
            ,'decline_question2':"¿Por qué rechazaste esta oferta?*"
            ,'decline_question3':"Si desea que nuestro equipo reconsidere la oferta presentada, cargue manualmente las siguientes fotos."
            ,'decline_question4':"4 cuadros exteriores de esquina"
            ,'decline_question5':"Foto Interior"
            ,'decline_question6':"Foto VIN"
            ,'decline_question7':"Foto de kilometraje"
            ,'decline_question8':"Nota: Los formatos de archivos de imagen admitidos son JPG, JPEG, PNG, etc."
            ,'Submit':"Entregar"
            ,'Click_to_upload':"Haga clic para cargar"
            ,'select_model_title':"Vaya, parece que falta el modelo de coche"
            }];
        else:
            inAuctionstatus =  [{'Home' : 'Home','How_it_Works':'How it Works','Faqs':'Faqs','About_Us':'About Us','Contact_Us':'Contact Us','header_btn_txt':'Get an Instant Offer on you car now'
            ,'sidebar_heading':'Get an Instant Offer','sidebar_description':"We'll keep track of your answers over here. You can jump back to a previous question any time."
            ,'sidebar_question1':'About your car'
            ,'sidebar_question2':'Location'
            ,'sidebar_question3':'Mileage'
            ,'sidebar_question4':"Body damage"
            ,'sidebar_question5':"Air bags"
            ,'sidebar_question6':"Starts and drives"
            ,'sidebar_question7':"Mechanical issues"
            ,'sidebar_question8':"Keys"
            ,'sidebar_question9':"Title Type"
            ,'sidebar_question10':"Water or fire damage"
            ,'sidebar_question11':"Offer amount"
            ,'sidebar_question12':"Accept"
            ,'sidebar_question13':"Current location"
            ,'sidebar_question14':"Your name and phone"
            ,'sidebar_question15':"Owner name"
            ,'sidebar_question16':"Payee name"
            ,'step_question1':"Tell us a little about your car"
            ,'year_label':"Year"
            ,'make_label':"Make"
            ,'model_label':"Model"
            ,'Autofill_with_VIN':"Autofill with VIN"
            ,'title_vin':"What's your car's VIN?"
            ,'subtitle_vin':"Using your VIN, we can quickly identify the year, make, model, and trim of your car."
            ,'back':"Back"
            ,'autofill':"Autofill"
            ,'where_is_your':"Where is your"
            ,'located':"located?"
            ,'zip_subtitle1':"Enter the ZIP code where your"
            ,'zip_subtitle2':"will be parked when we come to get it. (This info helps us determine the offer amount.)"
            ,'Enter_vehicle_location':"Enter vehicle location"
            ,'ZIP_code':"ZIP code"
            ,'mileage_title':"What's the mileage shown on the odometer?"
            ,'mileage_subtitle':"If you do not know the exact number that’s okay, as long as it is within 1,000 miles we will accept it."
            ,'Mileage_on_odometer':"Mileage on odometer"
            ,'Unable_to_verify':"Unable to verify"
            ,'next':"Next"
            ,'Does_your':"Does your"
            ,'damage_title':"have body damage or rust?"
            ,'damage_subtitle':"Body damage/rust refers to exterior imperfections larger than your fist."
            ,'damage_question1':"No, my vehicle is in good shape!"
            ,'damage_question2':"Yes, my vehicle has some damage or rust"
            ,'drive_title1':"Can you start and drive your"
            ,'drive_subtitle1':"This tells us about your"
            ,'drive_subtitle2':"condition and also helps us figure out the best tow truck to use for pickup. If it runs and drives our tow driver must be able to drive it when they pick it up."
            ,'mechanical_title1':"have any mechanical issues?"
            ,'mechanical_subtitle1':"We will buy your car no matter what! This just helps us determine how your vehicle will be handled."
            ,'title_title1':"have a clean title?"
            ,'title_subtitle1':"Every state is different, but if your vehicle has ever had an insurance company declare a total loss then it could have a salvage title."
            ,'firedamage_title1':"Has your"
            ,'firedamage_title2':"ever had any water or fire damage?"
            ,'firedamage_subtitle1':"Water and fire damage can be rare, we use this information to help us determine the best use of your vehicle."
            ,'Your':"Your"
            ,'offer_title1':"is exactly what we need!"
            ,'offer_title2':"We will pay you"
            ,'Sell_instantly':"Sell instantly"
            ,'Decline':"Decline"
            ,'offer_title3':"Accept the offer. We will come pick up your vehicle for FREE and pay you on the spot!"
            ,'start_from_begining':"Start from begining"
            ,'accept_title1':"Where should we pick up your"
            ,'Residence':"Residence"
            ,'Business':"Business"
            ,'Location_Name':"Location name"
            ,'Street_name':"Street name*"
            ,'Address_line_2':"Address line 2"
            ,'City':"City*"
            ,'Select_a_state':"Select a state*"
            ,'What_is_your_name_and_phone_number':"What is your name and phone number?"
            ,'Full_Name':"Full Name*"
            ,'Phone':"Phone*"
            ,'Alternate_Phone':"Alternate Phone"
            ,'owner_title1':"What is the owner(s) name shown on the title?"
            ,'owner_subtitle1':"List all the names on the title."
            ,'USE_MY_NAME':"USE MY NAME"
            ,'Full_Name_on_the_title':"Full Name on the title"
            ,'getting_paid':"Who's getting paid?"
            ,'Payee_Full_name':"Payee Full name"
            ,'You_are_all_finished':"You are all finished!"
            ,'reaching':"Someone will be reaching out soon!"
            ,'Have_another_car_to_sell':"Have another car to sell?"
            ,'Select_where_your':"Select where your"
            ,'has_rust_or_body_damage':"has rust or body damage"
            ,'airbag_title1':"Does your car currently have any airbags deployed?"
            ,'airbag_subtitle1':"Specify if your vehicle currently has the airbags deployed, this includes previous interior damage."
            ,'key_title1':"Do you have keys for your"
            ,'key_subtitle1':"This helps us know what to expect when we come to pick up your vehicle."
            ,'Calculating':"Calculating..."
            ,'Decline_offer':"Decline offer"
            ,'Name':"Name*"
            ,'Enter_name':"Enter name*"
            ,'Email':"Email*"
            ,'Enter_email':"Enter email*"
            ,'Phone_Number':"Phone Number*"
            ,'Enter_phone_number':"Enter phone number*"
            ,'decline_question1':"How much would you accept for your vehicle?*"
            ,'decline_question2':"Why did you declined this offer?*"
            ,'decline_question3':"if you would like our team to reconsider the offer given manually upload the following photos."
            ,'decline_question4':"4 corner outside pictures"
            ,'decline_question5':"Interior Photo"
            ,'decline_question6':"VIN Photo"
            ,'decline_question7':"Mileage Photo"
            ,'decline_question8':"Note : Supported image file formats are JPG, JPEG, PNG, etc."
            ,'Submit':"Submit"
            ,'Click_to_upload':"Click to upload"
            ,'select_model_title':"OOPS it looks like the car model is missing"
            }];

        return inAuctionstatus;

    def getCount(self, startDate, endDate):
        try:
            con = Setting.connect(self)
            cursor = con.cursor()
            
            startDate = changeStartDateFormat(startDate)
            endDate = changeEndDateFormat(endDate)

            cursor.execute('SELECT COUNT(id) from accepted_aps where status = "accept" AND created_at BETWEEN %s AND %s',(startDate, endDate))
            accepted_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(id) from accepted_aps where status_update = "Pending pick up" AND created_at BETWEEN %s AND %s',(startDate, endDate))
            pending_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(id) from accepted_aps where revised_price IS NOT NULL AND created_at BETWEEN %s AND %s',(startDate, endDate))
            offer_given_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(id) from accepted_aps where status_update = "At auction" AND created_at BETWEEN %s AND %s',(startDate, endDate))
            at_auction_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(id) from accepted_aps where status_update = "Canceled" AND created_at BETWEEN %s AND %s',(startDate, endDate))
            cancelled_count = cursor.fetchone()[0]
            
            if offer_given_count != 0:  
                accepted_percetage = round((accepted_count / offer_given_count) * 100)
                at_auction_percetage = round((at_auction_count / offer_given_count) * 100)
            else:
                accepted_percetage = 0
                at_auction_percetage = 0

            if accepted_count != 0:
                offer_given_percetage = round((at_auction_count / accepted_count) * 100)
                pending_percetage = round((pending_count / accepted_count) * 100)
                cancelled_percetage = round((cancelled_count / accepted_count) * 100)
            else:
                offer_given_percetage = 0
                pending_percetage = 0
                cancelled_percetage = 0
            
            return accepted_count,offer_given_count,pending_count,at_auction_count,cancelled_count,accepted_percetage,offer_given_percetage,pending_percetage,at_auction_percetage,cancelled_percetage

        except Exception as e:
            con.rollback()
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
        
    def getInquiryData(self, start_date, end_date, status, start, length, column, direction, search_value):
        """This function retrieves inquiry data from the database based on the specified parameters.
        
        Parameters:
            - start_date: The start date of the inquiry data.
            - end_date: The end date of the inquiry data.
            - status: The status of the inquiry data.
            - start: The starting index of the retrieved data.
            - length: The number of records to retrieve.
            - column: The column to sort the data by.
            - direction: The direction of the sorting (ASC or DESC).
            - search: The search term to filter the records.
        
        Returns:
            - inquiry_data: The retrieved inquiry data."""

        try:
            con = Setting.connect(self)
            cursor = con.cursor()

            if column == 'date':
                column = 'created_at'
            elif column == 'offerif':
                column = 'offer_id'
            elif column == 'revisedprice':
                column = 'revised_price'
            elif column == 'offer':
                column = 'status_update'
            else:
                column = 'created_at'

            start_date = changeStartDateFormat(start_date)
            end_date = changeEndDateFormat(end_date)

            search_terms = search_value.split()
            search_value = '%' + '%'.join(search_terms) + '%'

            concat_columns = "CONCAT(year, ' ', model, ' ', make_code, ' ')"

            if status == 'accept':
                status_condition = "status = 'accept'"
            elif status == 'notaccepted':
                status_condition = "revised_price IS NOT NULL"
            elif status == 'pending':
                status_condition = "status_update = 'Pending pick up'"
            elif status == 'atauction':
                status_condition = "status_update = 'At auction'"
            elif status == 'canceled':
                status_condition = "status_update = 'Canceled'"
            else:
                status_condition = "status != 'Decline'"
            query = """
                SELECT id, year, model, make_code, zip, original_price, status, user_city, user_state, created_at, revised_price, offer_id, dispatched, ref_id, status_update, utm_source, utm_medium, utm_campaign
                FROM accepted_aps
                WHERE created_at BETWEEN %s AND %s
                AND ({})
                AND (offer_id LIKE %s OR {} LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s)
                ORDER BY {} {}
                LIMIT %s OFFSET %s
            """.format(status_condition, concat_columns, column, direction)

            cursor.execute(query, (start_date, end_date, '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))

            inquiry_data = cursor.fetchall()

            
            # if status == 'accept':
            #     cursor.execute('SELECT id,year,model,make_code,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update from accepted_aps where status = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction),(status, start_date, end_date, '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))
            # elif status == 'notaccepted':
            #     cursor.execute('SELECT id,year,model,make_code,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update from accepted_aps where revised_price IS NOT NULL AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction),(start_date, end_date, '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))
            # elif status == 'pending':
            #     status = 'Pending pick up'
            #     cursor.execute('SELECT id,year,model,make_code,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update from accepted_aps where status_update = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction),(status, start_date, end_date, '%' + search_value + '%',  '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))
            # elif status == 'atauction':
            #     status = 'At auction'
            #     cursor.execute('SELECT id,year,model,make_code,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update from accepted_aps where status_update = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction),(status, start_date, end_date, '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))
            # elif status == 'canceled':
            #     status = 'Canceled'
            #     cursor.execute('SELECT id,year,model,make_code,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update from accepted_aps where status_update = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction), (status, start_date, end_date, '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', int(length), int(start)))
            # else:
                # cursor.execute('SELECT id, year, model, make_code, zip, original_price, status, user_city, user_state, created_at, revised_price, offer_id, dispatched, ref_id, status_update FROM accepted_aps WHERE created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make_code LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s'.format(column, direction), (start_date, end_date, '%' + search_value + '%', '%' + concat_columns + '%', '%' + concat_columns + '%', '%' + concat_columns + '%', '%' + search_value + '%', int(length), int(start)))
            # inquiry_data = cursor.fetchall()

            return inquiry_data

        except Exception as e:
            con.rollback()
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
        
    def get_total_records(self, start_date, end_date, status, search_value):
        # Retrieves the total number of records based on the given start date, end date, and status.
        # Args:
        #     start_date (str): The start date for the records.
        #     end_date (str): The end date for the records.
        #     status (str): The status of the records.
        # Returns:
        #     int: The total number of records.
        # Raises:
        #     Exception: If there is an error during the database operation.
        try:
            con = Setting.connect(self)
            cursor = con.cursor()

            start_date = changeStartDateFormat(start_date)
            end_date = changeEndDateFormat(end_date)

            search_terms = search_value.split()
            search_value = '%' + '%'.join(search_terms) + '%'

            concat_columns = "CONCAT(year, ' ', model, ' ', make_code, ' ')"

            query = '''
                SELECT COUNT(*)
                FROM accepted_aps
                WHERE created_at BETWEEN %s AND %s
                AND (
                    offer_id LIKE %s OR 
                    {} LIKE %s OR 
                    year LIKE %s OR 
                    make_code LIKE %s OR 
                    model LIKE %s OR 
                    revised_price LIKE %s
                )
            '''.format(concat_columns)

            query_params = [start_date, end_date, search_value, search_value, search_value,search_value, search_value, search_value]

            if status == 'accept':
                query = '''
                    SELECT COUNT(*)
                    FROM accepted_aps
                    WHERE created_at BETWEEN %s AND %s
                    AND status = %s
                    AND (
                        offer_id LIKE %s OR 
                        {} LIKE %s OR 
                        year LIKE %s OR 
                        make_code LIKE %s OR 
                        model LIKE %s OR 
                        revised_price LIKE %s
                    )
                '''.format(concat_columns)
                query_params.insert(2, status)
            elif status == 'notaccepted':
                query = '''
                    SELECT COUNT(*)
                    FROM accepted_aps
                    WHERE revised_price IS NOT NULL
                    AND created_at BETWEEN %s AND %s
                    AND (
                        offer_id LIKE %s OR 
                        {} LIKE %s OR 
                        year LIKE %s OR 
                        make_code LIKE %s OR 
                        model LIKE %s OR 
                        revised_price LIKE %s
                    )
                '''.format(concat_columns)
                query_params = [start_date, end_date, search_value, search_value, search_value,search_value, search_value, search_value]
            elif status in ('pending', 'atauction', 'canceled'):
                status_text = {
                    'pending': 'Pending pick up',
                    'atauction': 'At auction',
                    'canceled': 'Canceled'
                }
                query = '''
                    SELECT COUNT(*)
                    FROM accepted_aps
                    WHERE status_update = %s
                    AND created_at BETWEEN %s AND %s
                    AND (
                        offer_id LIKE %s OR 
                        {} LIKE %s OR 
                        year LIKE %s OR 
                        make_code LIKE %s OR 
                        model LIKE %s OR 
                        revised_price LIKE %s
                    )
                '''.format(concat_columns)
                query_params = [status_text[status], start_date, end_date, search_value, search_value, search_value, search_value, search_value, search_value]

            cursor.execute(query, query_params)
            total_records = cursor.fetchone()[0]

            return total_records

            

            # query_params = [start_date, end_date, search_value, search_value, search_value,
            # search_value, search_value, search_value]

            # if status == 'accept':
            #     # query = 'SELECT COUNT(*) FROM accepted_aps WHERE status = %s  AND created_at BETWEEN %s AND %s'
            #     query_params.insert(0, status)
            # elif status == 'notaccepted':
            #     query = 'SELECT COUNT(*) FROM accepted_aps WHERE revised_price IS NOT NULL AND created_at BETWEEN %s AND %s'
            # elif status in ('pending', 'atauction', 'canceled'):
            #     status_text = {
            #         'pending': 'Pending pick up',
            #         'atauction': 'At auction',
            #         'canceled': 'Canceled'
            #     }
            #     query = 'SELECT COUNT(*) FROM accepted_aps WHERE status_update = %s AND created_at BETWEEN %s AND %s'
            #     query_params.insert(0, status_text[status])
            # else:
            #     # query = 'SELECT COUNT(*) FROM accepted_aps WHERE created_at BETWEEN %s AND %s'

            # cursor.execute(query, query_params)
            # total_records = cursor.fetchone()[0]

            # return total_records
        except Exception as e:
            con.rollback()
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return 0