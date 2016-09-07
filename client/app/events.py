def paintEvent(self, event):
    qp = QPainter()
    qp.begin(self)
    qp.setFont(QFont('Decorative', 28))
    qp.drawText(event.rect(), Qt.AlignCenter, 'al;j saldjf l; jlk sdljf klsdjf sdkj  lkdjlk sdsf kl ksdjfl jlk sdljf klsdjf sdkj saf')
    qp.end()
