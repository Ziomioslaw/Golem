#!/usr/bin/python
#-*- coding: utf-8 -*-

class GolemActionModule:
    """Klasa bazowa do akcji Golema - listener do niego samego.
    
    Gdybym mógł, klasa byłaby abstakcyjną, albo interfacem.
    """
    def install(self, golem):
        """Moduł został właśnie zainstalowany.
        """
        self.golemInstance = golem
        
    def uninstall(self):
        """Moduł został właśnie wyinstalowany.
        """
        pass

    def getModulName(self):
        """Zwraca nazwę tego modułu akcji

        \return Nazwę modułu akcji.
        """
        pass

    def getVersionOfModule(self):
        """Zwraca numer wersji tego modułu
        
        \return Numer wersji modułu
        """
        pass

    def orderForModule(self, who, order):
        """Obsługa polecenia wydanego dla tego modułu
        \return string jaki ma zostać wyświetlony
        """
        pass

class WrongActionException(Exception):
    """Wyjątek występuje kiedy ktoś każe załadować golemowi nie
    prawidłowy obiekt akcji.
    """
    pass

if __name__ == "__main__":
    pass

