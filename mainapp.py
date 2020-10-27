from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
import sys
import periodictable
from mendeleev import element

from windows import main_window
from resources import neutron_dict


class elementValues():
    def __init__(self, element_str, scattering_dict, formulaUnitInput):
        self.isotope = element_str
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

        #connect buttons to functions
        self.buttonCalculate.clicked.connect(self.calculate_click)

        #set table headers on init
        self.tableInput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableInput.setHorizontalHeaderLabels(["Element", "Formula Units"])
        self.tableOutput.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableOutput.setHorizontalHeaderLabels([
            "Isotope", "Formula Units", "Atomic Weight (g/mol)", "Mass Fraction", "Number Density (mol/cc)",
            "Coh x-section", "Inc x-section", "Abs x-section", "Linear att. factor (/cm)"])
        # self.tableWidget.setHorizontalHeaderLabels([
        #     "Isotope", "Formula Units", "Atomic Weight (g/mol)", "Mass Fraction", "Number Density (mol/cc)",
        #     "Coh x-section", "Inc x-section", "Abs x-section", "Linear att. factor (/cm)"])

        self.scattering_dict = neutron_dict.get_neut_dict()

    def calculate_click(self):
        numRows = self.tableInput.rowCount()
        density = self.density_input.value()
        wavelength = self.wavelength_input.value()
        list_of_instances = []
        total_mass = 0
        for row in range(numRows):
            elemInputItem = self.tableInput.item(row, 0)
            formulaUnitInputItem = self.tableInput.item(row, 1)
            try:
                elemInput = str(elemInputItem.text().strip(" "))
                formulaUnitInput = int(formulaUnitInputItem.text())
                elem_instance = elementValues(elemInput, self.scattering_dict, formulaUnitInput)
                list_of_instances.append(elem_instance)
                total_mass += (formulaUnitInput * element(elemInput).atomic_weight)
            except:
                self.totalAttBox.setText("ERROR: input elements")

        self.tableOutput.setRowCount(len(list_of_instances))
        lin_att_total = 0
        for row, current_element in enumerate(list_of_instances):
            mendelem = element(current_element.isotope)  # use mendeleev package to get atomic info about element

            current_mass_fraction = (mendelem.atomic_weight * float(current_element.multiplier)) / total_mass

            current_number_density = (float(density) / mendelem.atomic_weight) * current_mass_fraction

            abs_x_section = (current_element.Absxs / 1.7980) * wavelength

            #matches NIST by multiplying only inc and abs by 0.6
            current_lin_att_fact = 0.6 * current_number_density * (current_element.Incxs + abs_x_section)
            lin_att_total += current_lin_att_fact

            self.tableOutput.setItem(row, 0, QTableWidgetItem(current_element.isotope))
            self.tableOutput.setItem(row, 1, QTableWidgetItem("{:d}".format(current_element.multiplier)))
            self.tableOutput.setItem(row, 2, QTableWidgetItem("{:f}".format(mendelem.atomic_weight)))
            self.tableOutput.setItem(row, 3, QTableWidgetItem("{:f}".format(current_mass_fraction)))
            self.tableOutput.setItem(row, 4, QTableWidgetItem("{:f}".format(current_number_density)))
            self.tableOutput.setItem(row, 5, QTableWidgetItem("{:f}".format(current_element.Cohxs)))
            self.tableOutput.setItem(row, 6, QTableWidgetItem("{:f}".format(current_element.Incxs)))
            self.tableOutput.setItem(row, 7, QTableWidgetItem("{:f}".format(abs_x_section)))
            self.tableOutput.setItem(row, 8, QTableWidgetItem("{:f}".format(current_lin_att_fact)))
            self.tableOutput.resizeColumnsToContents()
            self.tableOutput.resizeRowsToContents()

        self.totalAttBox.setText("{:f}".format(lin_att_total))


def main():
    app = QApplication(sys.argv)
    form = MainApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()