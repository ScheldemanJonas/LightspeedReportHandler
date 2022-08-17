from decimal import Decimal
from PyQt5.QtCore import QObject, pyqtSlot
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    @pyqtSlot(str)
    def add_files(self, value):
        self._model.add_files(value[0])

    @pyqtSlot(int)
    def delete_file(self, value):
        self._model.delete_file(value)

    @pyqtSlot()
    def calculate(self):
        d = []

        for file in self._model.files:
            report = Path(file)
            tree = ET.parse(report)
            root = tree.getroot()


            for receipt in root.iter("Receipt"):
                if Decimal(receipt.get('total')) > 0:

                    payment_t = next(receipt.iter("Payment"))
                    for t in receipt.iter("Tax"):

                        d.append(
                            {
                                "PaymentType": payment_t.get("type"),
                                "Tax": t.get("rate"),
                                "Amount": Decimal(t.get("revenueTotal")),
                            }
                        )
        df = pd.DataFrame(d)
        df = df.groupby(['PaymentType', 'Tax']).sum().reset_index()
        self._model.add_dataframe(df)
