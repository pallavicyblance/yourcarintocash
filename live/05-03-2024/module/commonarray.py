
class Commonarray:  
    def getbodydamage(self,):          
         #array  =  [{'shortname' : 'AO', 'name' : 'All Over'},{ 'shortname' : 'BN', 'name' : 'Burn'},{'shortname' : 'FR', 'name' : 'Front End'},{'shortname' : 'MN', 'name' : 'Minor dent/Scratches'}, {'shortname' : 'RE',  'name' : 'Rear End'},{'shortname' : 'SD', 'name' : 'Side Damage'},{'shortname' : 'TP', 'name' : 'Top/Roof' }];
         array  = [{'id' : '1', 'shortname' : 'AO', 'name' : 'All Over'},{ 'id' : '2', 'shortname' : 'BN', 'name' : 'Burn'},{ 'id' : '3', 'shortname' : 'FR', 'name' : 'Front End'},{'id' : '4', 'shortname' : 'MN', 'name' : 'Minor dent/Scratches'}, {'id' : '5', 'shortname' : 'RR',  'name' : 'Rear End'},{'id' : '6', 'shortname' : 'SD', 'name' : 'Side Damage'},{'id' : '7', 'shortname' : 'TP', 'name' : 'Top/Roof' }];
         return array;

    def getbodydamagesecondary(self,current_lan):          
      #array  =  [{'shortname' : 'AO', 'name' : 'All Over'},{ 'shortname' : 'BN', 'name' : 'Burn'},{'shortname' : 'FR', 'name' : 'Front End'},{'shortname' : 'MN', 'name' : 'Minor dent/Scratches'}, {'shortname' : 'RE',  'name' : 'Rear End'},{'shortname' : 'SD', 'name' : 'Side Damage'},{'shortname' : 'TP', 'name' : 'Top/Roof' }];
      if current_lan=='en':                 
        array  = [{'id' : '1', 'shortname' : 'No, my vehicle is in good shape!', 'name' : 'No, my vehicle is in good shape!'},{'id' : '2', 'shortname' : 'Yes, major engine issues', 'name' : 'Yes, major engine issues'},{'id' : '3', 'shortname' : 'Yes, major transmission issues', 'name' : 'Yes, major transmission issues'},{'id' : '4', 'shortname' : 'Yes, major frame issues', 'name' : 'Yes, major frame issues'}];
      elif current_lan=='undefined':                 
        array  = [{'id' : '1', 'shortname' : 'No, my vehicle is in good shape!', 'name' : 'No, my vehicle is in good shape!'},{'id' : '2', 'shortname' : 'Yes, major engine issues', 'name' : 'Yes, major engine issues'},{'id' : '3', 'shortname' : 'Yes, major transmission issues', 'name' : 'Yes, major transmission issues'},{'id' : '4', 'shortname' : 'Yes, major frame issues', 'name' : 'Yes, major frame issues'}];
      elif current_lan=='':
        array  = [{'id' : '1', 'shortname' : 'No, my vehicle is in good shape!', 'name' : 'No, my vehicle is in good shape!'},{'id' : '2', 'shortname' : 'Yes, major engine issues', 'name' : 'Yes, major engine issues'},{'id' : '3', 'shortname' : 'Yes, major transmission issues', 'name' : 'Yes, major transmission issues'},{'id' : '4', 'shortname' : 'Yes, major frame issues', 'name' : 'Yes, major frame issues'}];
      else:
        array  = [{'id' : '1', 'shortname' : 'No, my vehicle is in good shape!', 'name' : '¡No, mi vehículo está en buenas condiciones!'},{'id' : '2', 'shortname' : 'Yes, major engine issues', 'name' : 'Sí, problemas importantes con el motor'},{'id' : '3', 'shortname' : 'Yes, major transmission issues', 'name' : 'Sí, problemas importantes de transmisión'},{'id' : '4', 'shortname' : 'Yes, major frame issues', 'name' : 'Sí, problemas importantes con el marco'}];      
      return array;

    def gettypeoftitle(self, current_lan):
      #return  [{'shortname' : 'clean title', 'name' : 'I have a clean title'},{ 'shortname' : 'Salvage Rebuilt', 'name' : 'I have a salvage or rebuild title'},{'shortname' : 'Unknown', 'name' : 'I do not have a title'}];
      if current_lan=='en': 
        return  [{'id' : '1', 'shortname' : 'clean title', 'name' : 'Yes, I have a clean title'},{ 'id' : '2',  'shortname' : 'Salvage Rebuilt', 'name' : 'No, my title is branded (Salvage, rebuilt, lemon law, etc.)'},{ 'id' : '3', 'shortname' : 'Unknown', 'name' : 'No, I don’t have a title'}];
      elif current_lan=='undefined': 
        return  [{'id' : '1', 'shortname' : 'clean title', 'name' : 'Yes, I have a clean title'},{ 'id' : '2',  'shortname' : 'Salvage Rebuilt', 'name' : 'No, my title is branded (Salvage, rebuilt, lemon law, etc.)'},{ 'id' : '3', 'shortname' : 'Unknown', 'name' : 'No, I don’t have a title'}];
      elif current_lan=='': 
        return  [{'id' : '1', 'shortname' : 'clean title', 'name' : 'Yes, I have a clean title'},{ 'id' : '2',  'shortname' : 'Salvage Rebuilt', 'name' : 'No, my title is branded (Salvage, rebuilt, lemon law, etc.)'},{ 'id' : '3', 'shortname' : 'Unknown', 'name' : 'No, I don’t have a title'}];
      else:
        return  [{'id' : '1', 'shortname' : 'clean title', 'name' : 'Sí, tengo un título limpio'},{ 'id' : '2',  'shortname' : 'Salvage Rebuilt', 'name' : 'No, mi título es de marca (Salvamento, reconstrucción, ley limón, etc.)'},{ 'id' : '3', 'shortname' : 'Unknown', 'name' : 'No, no tengo título.'}];


    def getdoeskey(self, current_lan):
      if current_lan=='en':
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, I have the key'},{ 'id' : '2', 'shortname' : 'N', 'name' : 'No, I do not have a key'}];
      elif current_lan=='undefined':
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, I have the key'},{ 'id' : '2', 'shortname' : 'N', 'name' : 'No, I do not have a key'}];
      elif current_lan=='': 
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, I have the key'},{ 'id' : '2', 'shortname' : 'N', 'name' : 'No, I do not have a key'}];
      else:
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'si, tengo la llave'},{ 'id' : '2', 'shortname' : 'N', 'name' : 'No, no tengo llave'}];


    def getdrive(self, current_lan):
      if current_lan=='en':
        return  [{'id' : '1', 'shortname' : 'D', 'name' : 'Yes, it starts and drives'},{ 'id' : '2',  'shortname' : 'S', 'name' : 'No, it starts but does not drive'},{ 'id' : '3', 'shortname' : 'N', 'name' : 'No, it does not start'}];
      elif current_lan=='undefined':
        return  [{'id' : '1', 'shortname' : 'D', 'name' : 'Yes, it starts and drives'},{ 'id' : '2',  'shortname' : 'S', 'name' : 'No, it starts but does not drive'},{ 'id' : '3', 'shortname' : 'N', 'name' : 'No, it does not start'}];
      elif current_lan=='':
        return  [{'id' : '1', 'shortname' : 'D', 'name' : 'Yes, it starts and drives'},{ 'id' : '2',  'shortname' : 'S', 'name' : 'No, it starts but does not drive'},{ 'id' : '3', 'shortname' : 'N', 'name' : 'No, it does not start'}];
      else:            
        return  [{'id' : '1', 'shortname' : 'D', 'name' : 'Sí, arranca y conduce'},{ 'id' : '2',  'shortname' : 'S', 'name' : 'No, arranca pero no conduce'},{ 'id' : '3', 'shortname' : 'N', 'name' : 'No, no arranca'}];


    def getfiredamage(self, current_lan):
      if current_lan=='en':
        return  [{'id' : '1', 'shortname' : 'no', 'name' : 'No, it has never had any fire or water damage'},{ 'id' : '2',  'shortname' : 'W', 'name' : 'Yes, it had fire or water damage'}];
      elif current_lan=='undefined':
        return  [{'id' : '1', 'shortname' : 'no', 'name' : 'No, it has never had any fire or water damage'},{ 'id' : '2',  'shortname' : 'W', 'name' : 'Yes, it had fire or water damage'}];
      elif current_lan=='':
        return  [{'id' : '1', 'shortname' : 'no', 'name' : 'No, it has never had any fire or water damage'},{ 'id' : '2',  'shortname' : 'W', 'name' : 'Yes, it had fire or water damage'}];
      else:
        return  [{'id' : '1', 'shortname' : 'no', 'name' : 'No, nunca ha tenido daños por fuego o agua'},{ 'id' : '2',  'shortname' : 'W', 'name' : 'Sí, tuvo daños por fuego o agua'}];


    def getdeployedbags(self, current_lan):
      if current_lan=='en':
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, the airbags are deployed'},{ 'id' : '2',  'shortname' : 'N', 'name' : 'No, the airbags are not deployed'}];
      elif current_lan=='undefined':
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, the airbags are deployed'},{ 'id' : '2',  'shortname' : 'N', 'name' : 'No, the airbags are not deployed'}];
      elif current_lan=='':
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Yes, the airbags are deployed'},{ 'id' : '2',  'shortname' : 'N', 'name' : 'No, the airbags are not deployed'}];
      else:
        return  [{'id' : '1', 'shortname' : 'Y', 'name' : 'Sí, los airbags están desplegados'},{ 'id' : '2',  'shortname' : 'N', 'name' : 'No, los airbags no se activan'}];
      
    def getstate(self, ):
          return [{'id':'AL', 'name':'Alabama'},{'id':'AK', 'name':'Alaska'},{'id':'AZ', 'name':'Arizona'},{'id':'AR', 'name':'Arkansas'},{'id':'CA', 'name':'California'},{'id':'CO', 'name':'Colorado'},{'id':'CT', 'name':'Connecticut'},{'id':'DE', 'name':'Delaware'},{'id':'FL', 'name':'Florida'},{'id':'GA', 'name':'Georgia'},{'id':'HI', 'name':'Hawaii'},{'id':'ID', 'name':'Idaho'},{'id':'IL', 'name':'Illinois'},{'id':'IN', 'name':'Indiana'},{'id':'IA', 'name':'Iowa'},{'id':'KS', 'name':'Kansas'},{'id':'KY', 'name':'Kentucky'},{'id':'LA', 'name':'Louisiana'},{'id':'ME', 'name':'Maine'},{'id':'MD', 'name':'Maryland'},{'id':'MA', 'name':'Massachusetts'},{'id':'MI', 'name':'Michigan'},{'id':'MN', 'name':'Minnesota'},{'id':'MS', 'name':'Mississippi'},{'id':'MO', 'name':'Missouri'},{'id':'MT', 'name':'Montana'},{'id':'NE', 'name':'Nebraska'},{'id':'NV', 'name':'Nevada'},{'id':'NH', 'name':'New Hampshire'},{'id':'NJ', 'name':'New Jersey'},{'id':'NM', 'name':'New Mexico'},{'id':'NY', 'name':'New York'},{'id':'NC', 'name':'North Carolina'},{'id':'ND', 'name':'North Dakota'},{'id':'OH', 'name':'Ohio'},{'id':'OK', 'name':'Oklahoma'},{'id':'OR', 'name':'Oregon'},{'id':'PA', 'name':'Pennsylvania'},{'id':'RI', 'name':'Rhode Island'},{'id':'SC', 'name':'South Carolina'},{'id':'SD', 'name':'South Dakota'},{'id':'TN', 'name':'Tennessee'},{'id':'TX', 'name':'Texas'},{'id':'UT', 'name':'Utah'},{'id':'VT', 'name':'Vermont'},{'id':'VA', 'name':'Virginia'},{'id':'WA', 'name':'Washington'},{'id':'DC', 'name':'Washington D.C.'},{'id':'WV', 'name':'West Virginia'},{'id':'WI', 'name':'Wisconsin'},{'id':'WY', 'name':'Wyoming'}];
         
