// For conditions of distribution and use, see copyright notice in license.txt

#ifndef incl_HoveringNameController_h
#define incl_HoveringNameController_h

#include "ui_HoveringNameWidget.h"

#include <QWidget>
#include <CoreTypes.h>
#include <QRect>

class HoveringNameController: public QWidget, public Ui::hoveringName
{
    
Q_OBJECT

public:
    HoveringNameController();
    virtual ~HoveringNameController();

public slots:
    void SetText(const QString& text);
    QString GetText() const;
    void SetPixmap(QPixmap* icon);
    QPixmap* GetPixmap();

private:
    float text_padding_;
    QPixmap* pixmap_;
    QString text_;
};

#endif