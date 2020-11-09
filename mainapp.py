from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
import sys
import numpy
import pandas
from mendeleev import element

from windows import main_window
from resources import neutron_dict


class ElementValues:
    def __init__(self, element_str, scattering_dict, formulaUnitInput):
        self.isotope = element_str
        self.element = "".join([i for i in element_str if not i.isdigit()])
        self.conc = scattering_dict[element_str][0]
        self.CohB = scattering_dict[element_str][1]
        self.IncB = scattering_dict[element_str][2]
        self.Cohxs = scattering_dict[element_str][3]
        self.Incxs = scattering_dict[element_str][4]
        self.Scattxs = scattering_dict[element_str][5]
        self.Absxs = scattering_dict[element_str][6]
        self.multiplier = formulaUnitInput

    def __repr__(self):
        return self.isotope


class MainApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)

        # connect buttons to functions
        self.buttonCalculate.clicked.connect(self.calculate_click)

        # set table headers on init
        self.tableInput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableInput.setHorizontalHeaderLabels(["Element", "Formula Units"])
        self.tableOutput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableOutput.setHorizontalHeaderLabels([
            "Isotope", "Formula Units", "Atomic Weight (g/mol)", "Mass Fraction", "Number Density (mol/cc)",
            "Coh x-section", "Inc x-section", "Abs x-section", "Linear att. factor (/cm)"])

        # spin box changes row count
        self.spinTableRows.valueChanged.connect(self.table_row_change)

        self.scattering_dict = neutron_dict.get_neut_dict()

        ## todo add floating formula units

    def table_row_change(self):
        spin_row_value = self.spinTableRows.value()
        self.tableInput.setRowCount(spin_row_value)

    def calculate_click(self):
        numRows = self.tableInput.rowCount()
        density = self.density_input.value()
        wavelength = self.wavelength_input.value()
        list_of_instances = []
        total_mass = 0
        errorbool = False
        for row in range(numRows):
            elemInputItem = self.tableInput.item(row, 0)
            formulaUnitInputItem = self.tableInput.item(row, 1)
            try:
                elemInput = str(elemInputItem.text().strip(" "))
                print(elemInput)
                formulaUnitInput = float(formulaUnitInputItem.text())
                print(formulaUnitInput)
                if elemInput in self.scattering_dict:
                    elem_instance = ElementValues(elemInput, self.scattering_dict, formulaUnitInput)
                    list_of_instances.append(elem_instance)
                    total_mass += (formulaUnitInput * element(elem_instance.element).atomic_weight)
                else:
                    self.totalAttBox.setText("ERROR: item not in dictionary")
            except:         # add TypeError??
                errorbool = True
                self.totalAttBox.setText("ERROR: input elements")

        self.tableOutput.setRowCount(len(list_of_instances))
        lin_att_total = 0
        for row, current_element in enumerate(list_of_instances):
            mendelem = element(current_element.element)  # use mendeleev package to get atomic info about element

            current_mass_fraction = (mendelem.atomic_weight * float(current_element.multiplier)) / total_mass

            current_number_density = (float(density) / mendelem.atomic_weight) * current_mass_fraction

            abs_x_section = (current_element.Absxs / 1.7980) * wavelength

            # matches NIST by multiplying only inc and abs by 0.6
            current_lin_att_fact = 0.6 * current_number_density * (current_element.Incxs + abs_x_section)
            lin_att_total += current_lin_att_fact

            table_outputs = [current_element.isotope, "{:f}".format(current_element.multiplier),
                             "{:f}".format(mendelem.atomic_weight), "{:f}".format(current_mass_fraction),
                             "{:f}".format(current_number_density), "{:f}".format(current_element.Cohxs),
                             "{:f}".format(current_element.Incxs), "{:f}".format(abs_x_section),
                             "{:f}".format(current_lin_att_fact)]

            for column, data in enumerate(table_outputs):
                self.tableOutput.setItem(row, column, QTableWidgetItem(data))
            self.tableOutput.resizeColumnsToContents()
            self.tableOutput.resizeRowsToContents()

        if errorbool is False:
            self.totalAttBox.setText("{:f}".format(lin_att_total))
        else:
            pass


def main():
    app = QApplication(sys.argv)
    form = MainApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
