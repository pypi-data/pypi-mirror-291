# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:04:24 2024.

@author: gp
"""

# lsq_library.py

import numpy as np
from scipy import interpolate
from scipy.optimize import nnls
import matplotlib.pyplot as plt


class LSQAnalyzer:
    """
    Класс для анализа рентгеновских спектров методом наименьших квадратов.

    Позволяет находить процентное соотношение комбинации одних спектров в
    другом.
    """

    def __init__(self, x_range):
        """
        Инициализация анализатора LSQ.

        Parameters
        ----------
        x_range : tuple
            Диапазон значений x для LSQ анализа (начало, конец, шаг).

        Returns
        -------
        None.
        """
        self.x_lsq = np.arange(*x_range)
        self.x_model = np.arange(*x_range)
        self.data = {}
        self.results = {}

    def load_and_process(self, filename, tag):
        """
        Загрузка и обработка данных из файла.

        Parameters
        ----------
        filename : str
            Путь к файлу с данными.
        tag : str
            Метка для идентификации данных.

        Returns
        -------
        None.
        """
        input_data = np.loadtxt(filename)
        x_data = input_data[:, 0]
        y_data = input_data[:, 1]

        x_lsq = np.clip(self.x_lsq, x_data.min(), x_data.max())
        x_model = np.clip(self.x_model, x_data.min(), x_data.max())

        lsq = interpolate.interp1d(
            x_data,
            y_data,
            kind='cubic',
            bounds_error=False,
            fill_value="extrapolate"
        )(x_lsq)
        model = interpolate.interp1d(
            x_data,
            y_data,
            kind='cubic',
            bounds_error=False,
            fill_value="extrapolate"
        )(x_model)

        self.data[tag] = {'lsq': lsq, 'model': model, 'filename': filename}

    def perform_lsq(self, base, *calc_spectra):
        """
        Выполнение LSQ анализа.

        Parameters
        ----------
        base : str
            Метка базового спектра.
        *calc_spectra : str
            Метки расчетных спектров.

        Returns
        -------
        None.
        """
        calc_data = np.column_stack(
            [self.data[calc]['lsq'] for calc in calc_spectra]
            )
        result = nnls(calc_data, self.data[base]['lsq'])[0]
        coeff = result / sum(result) * 100
        model = sum(
            r * self.data[c]['model'] for r, c in zip(result, calc_spectra)
                    )
        key = f"{base}|||{'|||'.join(calc_spectra)}"
        self.results[key] = {'lsq': result, 'coeff': coeff, 'model': model}

    def save_results(self, filename):
        """
        Сохранение результатов в файл.

        Parameters
        ----------
        filename : str
            Путь к файлу для сохранения результатов.

        Returns
        -------
        None.
        """
        output = np.column_stack(
            [self.x_model] +
            [self.data[tag]['model'] for tag in self.data] +
            [self.results[key]['model'] for key in self.results]
        )
        header = ' '.join(
            ['x_model'] + list(self.data.keys()) + list(self.results.keys())
            )
        np.savetxt(filename, output, header=header, comments='')

    def plot_results(self):
        """
        Построение графиков результатов.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Объект фигуры с графиками.
        """
        num_results = len(self.results)
        fig, axes = plt.subplots(
            num_results,
            1,
            figsize=(8, 5 * num_results),
            squeeze=False
            )

        for i, (ax, (key, result)) in enumerate(
                zip(axes.flatten(), self.results.items()),
                1
                ):
            parts = key.split('|||')
            base, _ = parts[0], parts[1:]
            ax.plot(
                self.x_model,
                self.data[base]['model'],
                'b',
                label=f"Целевой спектр: {base}"
                )
            ax.plot(
                self.x_model,
                result['model'],
                'r',
                label='Модельный спектр (LSQ)'
                )
            ax.set_title(f"Сравнение {i}: {base} и LSQ модель")
            ax.legend()

        plt.tight_layout()
        return fig

    def format_coefficient(self, value):
        """
        Форматирование коэффициента.

        Parameters
        ----------
        value : float
            Значение коэффициента.

        Returns
        -------
        str
            Отформатированное значение коэффициента.
        """
        if np.isnan(value):
            return "0.00"
        return f"{value:.2f}"

    def input_data(self, input_dict):
        """
        Загрузка данных из словаря.

        Parameters
        ----------
        input_dict : dict
            Словарь с метками и путями к файлам данных.

        Returns
        -------
        None.
        """
        for tag, path in input_dict.items():
            self.data[tag] = {'filename': path}
            self.load_and_process(path, tag)

    def print_results(self):
        """
        Вывод результатов анализа.

        Returns
        -------
        None.
        """
        for i, (key, result) in enumerate(self.results.items(), 1):
            parts = key.split('|||')
            base = parts[0]
            calc_spectra = parts[1:]
            print(f"Сравнение {i}, коэффициенты для {base}:")
            for j, calc in enumerate(calc_spectra):
                print(
                    f"{calc}: {self.format_coefficient(result['coeff'][j])}%"
                    )
