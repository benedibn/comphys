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
  int n = atoi(argv[1]);        //Number of grid points
  char *outfilename;            //Declaration of variable we want to write v(x) to.
  outfilename = argv[2];        //The actual filename of the file we'll write v(x) to.
  double *a, *b, *c, *d, *l, *u, *q, *v, *y;    //Declaration of pointers to represent vectors.
  double h;                                     //Declaration of stepsize defined by the start_point, end_point and number of grid points n.
  double start_point = 0;
  double end_point = 1;
  h = (end_point-start_point)/( (double) n);    //Defines the stepsize.

  //Specification of the vectors used in the calculations using dynamic memory allocation.
  a = new double[n];
  b = new double[n];
  c = new double[n];
  d = new double[n];
  l = new double[n];
  u = new double[n];
  q = new double[n];
  v = new double[n];
  y = new double[n];

  //Used to time how long the program takes to finish.
  clock_t start, finish;
  start = clock();

  //Filling the arrays with the necessary values:
  for (int i = 0; i < n; i++){
    a[i] = -1.0;
    b[i] = 2.0;
    c[i] = -1.0;
    q[i] = f(i*h)*h*h;  //RHS of the matrix equation.
  }

  //step 1: LU-decomposition (A = LU)
  for (int i = 0; i < n; i++){
    if (i == 0){
      d[i] = b[i];
      u[i] = c[i];
    }
    else{
      l[i] = a[i-1]/d[i-1];
      d[i] = b[i] - l[i]*u[i-1];
      u[i] = c[i];
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
      v[i] = (y[i] - u[i]*v[i+1])/d[i];
    }
    i--;
  }

  //Main part of the program is finished, so we'll find the timestamp at finish and print it in the terminal.
  finish = clock();
  double timeused = (double) (finish-start)/(CLOCKS_PER_SEC);
  cout << "Total time = " << timeused << endl;

  //Deallocate memory. We'll keep v until it's written to a file.
  delete[] a;
  delete[] b;
  delete[] c;
  delete[] d;
  delete[] l;
  delete[] u;
  delete[] q;


  //Write v to a file
  ofile.open(outfilename);
  ofile << timeused << endl;
  for (int i = 0; i < n; i++){
    ofile << v[i] << endl;
  }
  ofile.close();      //Closes output file.
  delete[] v;
  return 0;
}

double f(double x){
  //RHS of the differential equation
  return 100*exp(-10*x);
}
