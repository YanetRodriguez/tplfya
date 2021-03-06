producciones = []
lista = []
first = []
follow = []
select = []
reservadas = ["lambda"]

class Gramatica:

    def __init__(self, gramatica):
        """Constructor de la clase.
        Parameters
        ----------
        gramatica : string
            Representación de las producciones de una gramática determinada.
            Ejemplo:
            "A:b A\nA:a\nA:A B c\nA:lambda\nB:b"
        """
        producciones = gramatica.split('\n')  # Genera una lista con cada producción
        self.gramatica = producciones
        self.first = Gramatica.calc_first(self.gramatica) #le paso las producciones como parámetro
        self.follows = Gramatica.calc_follows(self.gramatica)
        self.selects = Gramatica.calc_select(self.gramatica, self.first, self.follows)
        self.antecedentes = Gramatica.calculo_antecedentes(producciones)
        self.no_terminales = Gramatica.calculo_no_terminales(producciones)
        self.terminales = Gramatica.calculo_terminales(producciones)
        print('FIRST')
        print(self.first)
        print('FOLLOW')
        print(self.follows)
        print('SELECT')
        print(self.selects)

    def calculo_antecedentes(producciones):
        lista_antecedentes = []
        for p in producciones:
            antecedentes = p.split(':')
            lista_antecedentes.append(antecedentes[0])
        return lista_antecedentes

    def calculo_no_terminales(producciones):
        lista_antecedentes = []
        for p in producciones:
            antecedentes = p.split(':')
            if antecedentes[0] not in lista_antecedentes:
                lista_antecedentes.append(antecedentes[0])
        return lista_antecedentes

    def calculo_terminales(producciones):
        lista_terminales = []
        for p in producciones:
            division = p.split(":") #Divido ant de consec.
            consecuentes = division[1].split() #Consecuentes
            for c in consecuentes:
                if str.islower(c):
                    if c not in lista_terminales:
                        lista_terminales.append(c)
        return lista_terminales

    def calc_first(reglas):  # calculo de first para una regla pasada como parámetro.
        primeros = []
        FirstPorRegla = []
        indice = 0
        union = []
        lista_terminales = Gramatica.calculo_terminales(reglas)
        for r in reglas:  # Por cada regla
            primeros.clear()
            reglaActual = r
            divisionAC = r.split(":")  # Divido antecedente del consecuente
            consecuentes = divisionAC[1].split()  # Armo una lista con cada elemento del consecuente para esa regla
            primer_consecuente = list(consecuentes[0])
            if str.isupper(primer_consecuente[0]):  # Si la primera letra del primer consecuente empieza con mayúscula, es NT.
                no_terminal = consecuentes[0]  # Guardo el no terminal en una variable.
                aux_first = Gramatica.busq_terminal(no_terminal, r, reglas)
                #aux_first = busq_terminal(no_terminal, r, reglas)  # Busco los first del no terminal que tengo como first.
                for a in aux_first:
                    if a not in FirstPorRegla:
                        union.append(a)
                cadena_final = " ".join(union)
                FirstPorRegla.insert(indice, cadena_final)
            else:  # Si no comienza con mayúsculas, es un terminal -> ya tenemos el first de la regla.
                if consecuentes[0] == 'lambda':
                    terminal = 'lambda'
                else:
                    terminal = consecuentes[0]
                FirstPorRegla.insert(indice, terminal)  # Agrego en la posición indicada el terminal que es el first.
            indice += 1
        for elemento in range(0,len(FirstPorRegla)):
            hacerSplit = FirstPorRegla[elemento].split()
            listaNueva = list(hacerSplit)
            listaNueva2 = []
            for x in listaNueva:
                if x not in listaNueva2 and x in lista_terminales:
                    listaNueva2.append(x)
            FirstPorRegla[elemento] = listaNueva2
        return FirstPorRegla  # lista de first para cada antecedente

    def busq_terminal(noterminal, regla, producciones):
        concate = []
        concat = []
        primeros = []
        divisionRegla = regla.split(":")  # Divido la regla original en antecedente y consecuente
        divisionConsecuenteRegla = divisionRegla[1].split()  # Divido el consecuente en una lista. Cada pos un elemento.
        for p in producciones:  # por cada producción
            antecedenteconsecuente = p.split(":")  # Divido antecedente del consecuente
            consecuente = antecedenteconsecuente[1].split()  # Divido los consecuentes de esa regla.
            if antecedenteconsecuente[0] == noterminal:  # Si el antecedente es igual al no terminal que traigo del otro método
                if str.islower(consecuente[0]):  # Si el primer consecuente es minúscula
                    if consecuente[0] == 'lambda':  # Si es igual a lambda, veo si sigue en la regla original otra cosa.
                        ind = 0
                        for x in divisionConsecuenteRegla:  # por cada consecuente de la regla original, pregunto si es igual al NT, para id si es el ultimo
                            if x == noterminal:
                                if x == divisionConsecuenteRegla[-1]:  # Si es el último elemento de la lista, significa que no viene más nada
                                    terminal = 'lambda'
                                    if terminal not in primeros:  # Guardo lambda en la lista de first.
                                        primeros.append(terminal)
                                else:  # Si ese NT no es el último elemento, puede venir otro NT o un terminal.
                                    elemento_siguiente = list(divisionConsecuenteRegla[ind + 1])
                                    if str.isupper(elemento_siguiente[0]):  # Si es mayúscula, calcular firsts.
                                        auxiliar = Gramatica.busq_terminal(divisionConsecuenteRegla[ind + 1], regla, producciones)
                                        if 'lambda' in auxiliar:
                                            primeros.append('lambda')
                                        for u in auxiliar:
                                            for m in u:
                                                if m not in primeros:
                                                    concat.append(m)
                                        auxiliar2 = " ".join(concat)
                                        primeros.append(auxiliar2)
                                    else:  # Es minúsculas, se agrega directamente.
                                        terminal = elemento_siguiente
                                        if terminal not in primeros:  # Lo agrego a los first
                                            primeros.append(elemento_siguiente)
                            ind = ind + 1
                    else:  # Si es distinto de lambda
                        terminal = consecuente[0]
                        if terminal not in primeros:
                            primeros.append(terminal)
                else:
                    elemento = list(consecuente[0])
                    if str.isupper(elemento[0]):
                        auxiliar3 = Gramatica.busq_terminal(consecuente[0], p,
                                                            producciones)  # ver que cambia si pongo p o r
                        for m in auxiliar3:
                            if m not in primeros:
                                concate.append(m)
                        auxiliar3 = " ".join(concate)
                        primeros.append(auxiliar3)
        return primeros

    def calc_follows(reglas):
        lista_follows = []
        lista_antecedentes = Gramatica.calculo_no_terminales(reglas)
        for a in range(0, len(lista_antecedentes)):
            lista_follows.insert(a, [])
        for i in range(0, len(lista_antecedentes)):  # POR CADA ANTECEDENTE
            if i == 0:
                lista_follows[i].append('$')  # agrego $ en la posicion 0
            for x in range(0, len(reglas)):  # recorro cada regla a ver si lo encuentro como consecuente en alguna.
                division = reglas[x].split(":")  # Antecedente y consecuente
                consecuentes = division[1].split()  # lista de consecuentes
                for c in range(0, len(consecuentes)):  # por cada consecuente de la regla en la que estoy.
                    if consecuentes[c] == lista_antecedentes[i]:  # Si encuentro el antecedente como consecuente
                        if consecuentes[c] == consecuentes[-1]:  # pregunto si es el último elemento de la lista.
                            ant = division[0]  # Antecedente de la regla donde encontre ese NT como ultimo elemento.
                            for n in range(0, len(lista_antecedentes)):
                                if lista_antecedentes[n] == ant:
                                    for elemento in lista_follows[n]:
                                        if elemento not in lista_follows[i]:
                                            lista_follows[i].extend(elemento)
                        else:  # Si no es el último elemento.
                            siguiente = consecuentes[c + 1]  # elemento siguiente
                            if str.islower(siguiente):  # si el siguiente elemento es minusculas, es un terminal.
                                lista_follows[i].append(siguiente)
                            else:  # buscar los first de ese elemento.
                                aux_first = Gramatica.calc_first(reglas)
                                for m in range(0, len(reglas)):
                                    dividir = reglas[m].split(":")
                                    if dividir[0] == siguiente:
                                        if aux_first[m] not in lista_follows[i]:
                                            lista_follows[i].extend(aux_first[m])
        return lista_follows

    def calc_select(reglas, listaFirst, listaFollow):
        SelectsPorRegla = []
        lista_antecedentes = []
        lista_no_terminales = []
        for item in range(0, len(listaFirst)):
            if 'lambda' not in listaFirst[item]:
                SelectsPorRegla.insert(item, listaFirst[item])
            else: #en item hay un lambda
                lista_antecedentes = Gramatica.calculo_antecedentes(reglas)
                lista_no_terminales = Gramatica.calculo_no_terminales(reglas)
                antecedente = lista_antecedentes[item]
                for i in range(0,len(lista_no_terminales)):
                    if lista_no_terminales[i] == antecedente:
                        SelectsPorRegla.insert(item,listaFollow[i])
        return SelectsPorRegla

    """
            for elemento in range(0,len(FirstPorRegla)):
            hacerSplit = FirstPorRegla[elemento].split()
            listaNueva = list(hacerSplit)
            FirstPorRegla[elemento] = listaNueva
    """

    def isLL1(self):
        """
        Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.
        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        DEVOLVER BOOLEANO.
        No recibe parámetros. Devuelve booleano de acuerdo a si es o no LL(1)
        Calcular first, follows y selects de la gramática que ingresó.
        De ahí, mirar selects y y ver si son o no disyuntos: de ahí el booleano
        """

        """
        conjunto_select = []
        posicion = 0
        antecedente = self.antecedentes[0] #Guardo como primer antecedente el primer antecedente de las reglas, el distinguido
        for a in range(0, len(self.no_terminales)):
            conjunto_select.insert(a, [])
        print(conjunto_select)
        for e in range(0,len(self.antecedentes)):
            for a in range(0,len(self.no_terminales)):
                if self.no_terminales[a] == self.antecedentes[e]:
                    conjunto_select[a].append(self.selects[e])
        print(conjunto_select)
                for c in range(0,len(conjunto_select)):
            nuevaLista = conjunto_select[c]
            nuevaLista2 = nuevaLista.split()
        print(conjunto_select)
         for a in range(0,len(self.no_terminales)):
            
            


        for a in range(0,len(self.no_terminales)): #Por cada antecedente de la regla.
            if self.no_terminales[a] == antecedente:
                conjunto_select[posicion].append(self.selects[a])
            else:
                posicion=posicion+1
                antecedente = self.no_terminales[a]
        print(conjunto_select)
        """




    def parse(self, cadena):
        """Retorna la derivación para una cadena dada utilizando las
           producciones de la gramática y los conjuntos de Fi, Fo y Se
           obtenidos previamente.
        Parameters
        ----------
        cadena : string
            Cadena de entrada.
            Ejemplo:
            babc
        Returns
        -------
        devivacion : string
            Representación de las reglas a aplicar para derivar la cadena
            utilizando la gramática.
        -Método Parse, recibe como parámetro una cadena de texto, string.
        A partir de ese string devuelve una representación de las derivaciones
        que se harian a partir de la gramática que se está utilizando.
        Partiendo del distinguido, todas las reglas que se aplicarían
        hasta llegar a esa cadena. X=>X Y=>b Y=>b d
        """
        pass

#reglas = "S:A B\nA:a A\nA:c\nA:lambda\nB:b B\nB:d" #ESTÁ OK.
reglas = "S:X Y Z\nX:a\nX:b\nX:lambda\nY:a\nY:d\nY:lambda\nZ:e\nZ:f\nZ:lambda" #REVISAR FOLLOWS Y SELECTS.
#reglas = 'S:A b\nS:B a\nA:a A\nA:a\nB:a' #ESTA OK
#reglas = 'S:A B c\nA:a\nA:lambda\nB:b\nB:lambda' #VER FOLLOWS Y SELECTS.
#reglas = "S:a S e\nS:A z\nA:B\nA:b B e\nA:C\nB:c C e\nB:d\nC:b" #VER ESTE CASO NO ES LL1.
nuevaGramatica = Gramatica(reglas)