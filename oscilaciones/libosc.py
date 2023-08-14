import numpy as np
from numpy import cos, sin, pi, sqrt, arctan
import plotly.graph_objects as go


class oscilador:

    def __init__(self, **params):
        self.m = params.get('m', 0.1)
        self.k = params.get('k', np.nan)
        if not np.isnan(self.k):
            self.w0 = params.get('w0', np.nan)
            if not np.isnan(self.w0):
                print("El valor de w0 no se tuvo en cuenta.")
            self.w0 = sqrt(self.k / self.m)
        else:
            self.w0 = params.get('w0', 2*pi)
            self.k = self.m * self.w0 * self.w0

        self.g = params.get('g', 0)
        self.x0 = params.get('x0', 0.1)
        self.v0 = params.get('v0', 0)

        self.wp = sqrt(self.w0 * self.w0 - self.g * self.g)
        self.wRA = sqrt(self.w0 * self.w0 - 2 * self.g * self.g)

        # Forzado: F_o, w, A estacionario, delta
        if self.g == 0:
            self.F0 = 1
            self.w = params.get('w', 0)
            if self.w > 0:
                print("No hay disipación, el valor de w se forzó a cero.")
            self.w = 0
        else:
            self.F0 = params.get('F0', 1)
            self.w = params.get('w', 0)

        # Calcular A y Aest, d
        # self.A =
        self.Aest = self.calcular_Aest(self.w)
        self.d = self.calcular_delta()


    def __str__(self):
        #if np.isnan(self.data):
        #    self.text_data = "No images loaded."
        #else:
        #    self.text_data = type(self.data)
        #return f"med Movie object\n\ndata = {self.text_data}\nx0 = {self.x0}\ny0 = {self.y0}\nDimensions = {self.L} x {self.L}"
        out = "Sistema oscilatorio:\n\n"
        out = out + "m = " + str(self.m) + " kg \n"
        out = out + "k = " + str(self.k) + " N/m \n"
        out = out + "w0 = " + str(self.w0) + " 1/s \n"
        out = out + "gamma = " + str(self.g) + " 1/s \n"
        out = out + "w' = " + str(self.wp) + " 1/s \n"
        out = out + "wRA = " + str(self.wRA) + " 1/s \n"
        out = out + "F0 = " + str(self.F0) + " N \n"
        out = out + "w = " + str(self.w) + " 1/s \n"
        out = out + "Aest = " + str(self.Aest * 100) + " cm \n"
        out = out + "delta = " + str(self.d) + " rad \n"
        # return f"Sistema oscilatorio:\n\nNumber of frames = {self.data.shape[0]}\nx0 = {self.x0}\ny0 = {self.y0}\nDimensions = {self.L} x {self.L}"
        return out

    def calcular_Aest(self, w):
        """Amplitud en régimen estacionario

        Calcula la amplitud para cualquier valor de w, no solo del w guradado.
        Conveniente para producir gráficos de amplitud con las características del sistema.

        Parameters
        ----------
        w : float
            Frecuencia externa.

        Returns
        -------
        float
        """
        gw2 = (2 * self.g * w) * (2 * self.g * w)
        wow = (self.w0 * self.w0 - w * w) * (self.w0 * self.w0 - w * w)
        Fm = self.F0 / self.m
        return Fm/sqrt(wow+gw2)

    def calcular_delta(self):
        """Constante de fase (delta) en régimen estacionario

        Parameters
        ----------

        Returns
        -------
        float
        """
        gw2 = 2 * self.g * self.w
        wow = self.w0 * self.w0 - self.w * self.w
        if wow != 0:
            at = arctan(gw2 / wow)
        else:
            at = pi / 2
        if at < 0:
            at = at + pi
        return at

    def F(self, t):
        """F(t)

        Parameters
        ----------
        t : float
            El tiempo.

        Returns
        -------
        float
        """

        return self.F0*cos(self.w*t)

    def xest(self, t):
        """x(t) en régimen estacionario

        Parameters
        ----------
        t : float
            El tiempo.

        Returns
        -------
        float
        """

        return self.Aest*cos(self.w*t - self.d)

    def vest(self, t):
        """v(t) en régimen estacionario

        Parameters
        ----------
        t : float
            El tiempo.

        Returns
        -------
        float
        """

        return -1*self.w*self.Aest*sin(self.w*t - self.d)

