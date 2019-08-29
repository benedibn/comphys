#include <iostream>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include "time.h"

using namespace std;
ofstream ofile;

//double f(double); //Declaration of the RHS of the differential equation to be solved.
void f(double, double, double&);
void LU_decomposition(double*, double*, double*, double*, double*, double*, int);
void Forward_substitution(double*, double*, double*, int);
void Back_substitution(double*, double*, double*, double*, int);
void write_to_file(double*, char*, double, int);

int main(int argc, char* argv[]){
  //Declaration of variables.
  int n = atoi(argv[1]);        //Number of grid points
  char *outfilename_solution;            //Declaration of variable we want to write v(x) to.
  outfilename_solution = argv[2];        //The actual filename of the file we'll write v(x) to.
  double *a, *b, *c, *d, *l, *u, *q, *v, *y;    //Declaration of pointers to represent vectors.
  double h;                                     //Declaration of stepsize defined by the start_point, end_point and number of grid points n.
  double start_point = 0.0;
  double end_point = 1.0;
  h = (end_point-start_point)/( (double) n + 1.0);    //Defines the stepsize.


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
  double h_squared = h*h; //Multiplication factor that reduces number of flops in the for-loop.
  for (int i = 0; i < n; i++){
    a[i] = -1.0;
    b[i] = 2.0;
    c[i] = -1.0;
    double x = ((double) i + 1.0)*h;
    //q[i] = f(i*h)*h*h;  //RHS of the matrix equation.
    f(x, h_squared, q[i]); //Call by reference to speed up execution.
  }

  //Step 1: LU-decomposition of A on the form A = LU.
  LU_decomposition(a, b, c, d, l, u, n);

  //Step 2: Forward substituion, solving Ly = q
  Forward_substitution(y, q, l, n);

  //Step 3: Back-substitution, solving Uv = y
  Back_substitution(v, y, u, d, n);

  //Compute the time interval the main algorithm took to complete.
  finish = clock();
  double timeused = (double) (finish-start)/(CLOCKS_PER_SEC);
  cout << "Total time = " << timeused << " s" << endl;

  //Write result to file.
  write_to_file(v, outfilename_solution, timeused, n);
  return 0;
}


void LU_decomposition(double* a, double* b, double* c, double* d, double* l, double* u, int n){
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
  //No more use for a, b and c so we deallocate their memory here.
  delete[] a;
  delete[] b;
  delete[] c;

  return;
}

void Forward_substitution(double* y, double* q, double* l, int n){
  for (int i = 0; i < n; i++){
    if (i == 0){
      y[i] = q[i];
    }
    else{
      y[i] = q[i] - l[i]*y[i-1];
    }
  }

  //q and l has served its purpose and is thus deallocated.
  delete[] q;
  delete[] l;
  return;
}

void Back_substitution(double* v, double* y, double* u, double* d, int n){
  for (int i = n-1; i > 0; i--){
    if (i == n-1){
      v[i] = y[i]/d[i];
    }
    else{
      v[i] = (y[i] - u[i]*v[i+1])/d[i];
    }
  }

  //Deallocates y and d as their no longer needed.
  delete[] y;
  delete[] d;
  delete[] u;

  return;
}

void write_to_file(double* v, char* outfilename, double timeused, int n){
  ofile.open(outfilename);
  ofile << timeused << endl;
  for (int i = 0; i < n; i++){
    ofile << v[i] << endl;
  }
  ofile.close();

  delete[] v;
  return;

}

void f(double x, double h, double& vector_element){
   vector_element = 100*exp(-10*x)*h;
   return;
}
