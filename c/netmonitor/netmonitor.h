#ifndef NETMONITOR_H
#define NETMONITOR_H

#include <qlistview.h>
#include <qmainwindow.h>
#include <qstring.h>
#include <qprogressbar.h>
#include <qcombobox.h>

#include <map>
#include <string>

using namespace std;

struct InterfaceData {
  int rstart;
  int tstart;
  int rlast;
  int tlast;
  int rmaximum;
  int tmaximum;
  QListViewItem *ritem;
  QListViewItem *titem;
  double timestart;
  bool active;
};

typedef map<QString, InterfaceData*> Table;

class NetMonitor: public QMainWindow {

  Q_OBJECT

public:
  NetMonitor();
  ~NetMonitor();
public slots:
  void update();
private:
  void extract(string &line, QString &name, int &rbytes, int &tbytes) const;
  int getInt(string &line) const;

  double lasttime;
  Table table;
  QListView *rec;
  QListView *tra;
  QProgressBar *rdial;
  QProgressBar *tdial;
  QComboBox *combo;
};

#endif
