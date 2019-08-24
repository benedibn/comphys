#include <iostream>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include "time.h"

using namespace std;
ofstream ofile;

double f(double); //Declaration of the RHS of the differential equation to be solved.

int main(int argc, char* argv[]){
  int n = atoi(argv[1]);
  char *outfilename;
  outfilename = argv[2];
  double  *d, *l, *q, *v, *y;
  double h;
  double start_point = 0;
  double end_point = 1;
  h = (end_point-start_point)/( (double) n);
  double a = -1.0;
  double c = -1.0;
  double b = 2.0;
  double u = c;
  d = new double[n];
  l = new double[n];
  q = new double[n];
  v = new double[n];
  y = new double[n];
  //Filling the arrays with the necessary values:
  clock_t start, finish;
  start = clock();
  for (int i = 0; i < n; i++){
    //Filling up the matrix.
    q[i] = f(i*h)*h*h;  //RHS of the matrix equation.
  }

  //step 1: LU-decomposition (A = LU)
  for (int i = 0; i < n; i++){
    if (i == 0){
      d[i] = b;
    }
    else{
      l[i] = a/d[i-1];
      d[i] = b - l[i]*u;
    }
  }

  // Step 2: Forward substitution (solving Ly = q)
  for (int i = 0; i < n; i++){
    if (i == 0){
      y[i] = q[i];
    }
    else{
      y[i] = q[i] - l[i]*y[i-1];
    }
  }

  //Step 3: Backward substitution (Solving Uv = y)
  int i = n-1;
  while (i > 0){
    if (i == n-1){
      v[i] = y[i]/d[i];
    }
    else{
      v[i] = (y[i] - u*v[i+1])/d[i];
    }
    i--;
  }

  //Main program is finished, so we'll find the timestamp at finish.
  finish = clock();
  double timeused = (double) (finish-start)/(CLOCKS_PER_SEC);
  cout << "Total time = " << timeused << endl;

  //Deallocate memory. We'll keep v until it's written to a file.
  delete[] d;
  delete[] l;
  delete[] q;


  //Write v to a file
  ofile.open(outfilename);
  for (int i = 0; i < n; i++){
    ofile << v[i] << endl;
  }

  delete[] v;
  return 0;
}

double f(double x){
  //RHS of the differential equation
  return 100*exp(-10*x);
}
