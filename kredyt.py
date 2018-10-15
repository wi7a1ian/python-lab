class Kredyt:
    def __init__(self, cenaMieszkania, wkladWlasny, okresKredytowania, oprocentowanie, oplatyPoczatkowe = 0):
        self.cenaMieszkania = cenaMieszkania
        self.wkladWlasny = wkladWlasny
        self.kredyt = cenaMieszkania - wkladWlasny
        self.okresKredytowania = okresKredytowania
        self.rata = self.kredyt/self.okresKredytowania
        self.oprocentowanie = oprocentowanie
        self.pozostalyOkres = okresKredytowania
        self.pozostalyKredyt = self.kredyt
        self.sumaOdsetek = oplatyPoczatkowe

    def Splacaj(self, okres=None):
        if okres is None:
            okres = self.pozostalyOkres
            
        if(okres > self.pozostalyOkres):
            raise Exception("Zbyt dlugi okres splat")
        else:
            for i in range(okres):
                self.sumaOdsetek += self.pozostalyKredyt * self.oprocentowanie / 100 / 12
                self.pozostalyKredyt -= self.rata
            self.pozostalyOkres -= okres
        return (self.pozostalyOkres, self.pozostalyKredyt)

    def Nadplac(self, kwota):
        if kwota >= self.pozostalyKredyt:
            self.pozostalyKredyt = 0
            self.pozostalyOkres = 0
        else:
            self.pozostalyKredyt -= kwota
            self.rata = self.pozostalyKredyt / self.pozostalyOkres
        return (self.pozostalyOkres, self.pozostalyKredyt)

    def SumaOdsetek(self):
        return self.sumaOdsetek

oproc = 3.9

x = Kredyt(228000.0, 45600, 12*30, oproc, 7000)
x.Splacaj()
print("30lat", round(x.SumaOdsetek(), 2))

x = Kredyt(228000.0, 45600, 12*20, oproc, 7000)
x.Splacaj()
print("20lat", round(x.SumaOdsetek(), 2))

x = Kredyt(228000.0, 45600, 12*15, oproc, 6000)
x.Splacaj()
print("15lat", round(x.SumaOdsetek(), 2))

x = Kredyt(228000.0, 45600, 12*10, oproc, 6000)
x.Splacaj()
print("10lat", round(x.SumaOdsetek(), 2))

x = Kredyt(228000.0, 45600, 12*30, oproc, 7000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
(okres, pozostalyKredyt) = x.Nadplac(50000)
x.Splacaj()
print("30latNadplataPrzy10", round(x.SumaOdsetek(), 2), "do nadplaty", 50000)

x = Kredyt(228000.0, 45600, 12*20, oproc, 7000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
(okres, pozostalyKredyt) = x.Nadplac(50000)
x.Splacaj()
print("20latNadplataPrzy10", round(x.SumaOdsetek(), 2), "do nadplaty", 50000)

x = Kredyt(228000.0, 45600, 12*15, oproc, 6000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
(okres, pozostalyKredyt) = x.Nadplac(50000)
x.Splacaj()
print("15latNadplataPrzy10", round(x.SumaOdsetek(), 2), "do nadplaty", 50000)

x = Kredyt(228000.0, 45600, 12*30, oproc, 7000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
x.Nadplac(pozostalyKredyt)
print("30latSplataPrzy10", round(x.SumaOdsetek(), 2), "do splaty", round(pozostalyKredyt, 2))


x = Kredyt(228000.0, 45600, 12*20, oproc, 7000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
x.Nadplac(pozostalyKredyt)
print("20latSplataPrzy10", round(x.SumaOdsetek(), 2), "do splaty", round(pozostalyKredyt, 2))

x = Kredyt(228000.0, 45600, 12*15, oproc, 6000)
(okres, pozostalyKredyt) = x.Splacaj(12*10)
x.Nadplac(pozostalyKredyt)
print("15latSplataPrzy10", round(x.SumaOdsetek(), 2), "do splaty", round(pozostalyKredyt, 2))

x = Kredyt(228000.0, 45600, 12*20, oproc, 7000)
x.Splacaj(12*5)
x.Nadplac(20000)
x.Splacaj(12*5)
x.Nadplac(20000)
x.Splacaj(12*5)
x.Nadplac(20000)
x.Splacaj()
print("*", round(x.SumaOdsetek(), 2))

