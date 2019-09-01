#include <iostream>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include "time.h"

using namespace std;
ofstream ofile_solution, ofile_errors, ofile_time;

//double f(double); //Declaration of the RHS of the differential equation to be solved.
void f(double, double, double&);
void LU_decomposition(double*, double*, double*, double*, double*, double*, int);
void Forward_substitutionLU(double*, double*, double*, int);
void Back_substitutionLU(double*, double*, double*, double*, int);
void Forward_substitution(double*, double*, double*, double*, int);
void Back_substitution(double*, double*, double*, double*, int);
void closed_form_solution(double, double&);
void compute_errors(double*, double*, double*, int);

int main(int argc, char* argv[]){
  //Declaration of variables.
  int n = atoi(argv[1]);        //Number of grid points
  char *outfilename_solution, *outfilename_errors, *outfilename_time; //Declaration of filenames
  outfilename_solution = argv[2];        //The actual filename of the file we'll write v(x) to.
  outfilename_errors = argv[3];          //Filename we'll write the computed relative errors to.
  outfilename_time = argv[4];
  double *a, *b, *c, *d, *l, *u, *q, *v, *y, *DE_solution, *errors;    //Declaration of pointers to represent vectors.
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
  DE_solution = new double[n];
  errors = new double[n];

  //Filling the arrays with the necessary values:
  double h_squared = h*h; //Multiplication factor that reduces number of flops in the for-loop.
  for (int i = 0; i < n; i++){
    a[i] = -1.0;
    b[i] = 2.0;
    c[i] = -1.0;
    double x = ((double) i + 1.0)*h;
    //q[i] = f(i*h)*h*h;  //RHS of the matrix equation.
    f(x, h_squared, q[i]); //Call by reference to speed up execution.
    closed_form_solution(x, DE_solution[i]);
  }

  clock_t start, finish;    //Declaration of variables to time the main algorithm
  start = clock();          //Starts the clock.

  //Main algorithm:

  //Step 1: LU-decomposition of A on the form A = LU.
  //LU_decomposition(a, b, c, d, l, u, n);

  //Step 2: Forward substituion, solving Ly = q
  //Forward_substitutionLU(y, q, l, n);
  Forward_substitution(a, b, c, q, n);

  //Step 3: Back-substitution, solving Uv = y
  //Back_substitutionLU(v, y, u, d, n);
  Back_substitution(v, b, c, q, n);


  //Compute the time interval the main algorithm took to complete.
  finish = clock();     //Stops the clock
  double timeused = (double) (finish-start)/(CLOCKS_PER_SEC);   //Computes the time elapsed for the main algorithm to finish
  cout << "Total time = " << timeused << " s" << endl;          //Prints the time elapsed to screen.
  //Writes the time elapsed to a file
  ofile_time.open(outfilename_time);
  ofile_time << timeused << endl;
  ofile_time.close();


  //Compute errors
  compute_errors(errors, v, DE_solution, n);

  //Write computed solution and computed relative errors to their own files.
  ofile_solution.open(outfilename_solution);
  ofile_errors.open(outfilename_errors);
  for (int i = 0; i < n; i++){
    ofile_solution << v[i] << endl;
    ofile_errors << errors[i] << endl;
  }
  ofile_solution.close();
  ofile_errors.close();
  delete[] v;
  delete[] errors;


  //Write the time elapsed to a file
  ofile_time.open(outfilename_time);
  ofile_time << timeused << endl;
  ofile_time.close();

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

void Forward_substitutionLU(double* y, double* q, double* l, int n){
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

void Back_substitutionLU(double* v, double* y, double* u, double* d, int n){
  for (int i = n-1; i >= 0; i--){
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

void Forward_substitution(double* a, double* b, double* c, double* y, int n){
  for (int i = 1; i < n; i++){
    b[i] -= a[i-1]*c[i-1]/b[i-1];
    y[i] -= a[i-1]*y[i-1]/b[i-1];
  }
  delete[] a;
  return;
}

void Back_substitution(double* x, double* b, double* c, double* y, int n){
  for (int i = n-1; i >= 0; i--){
    if (i == n-1){
      x[i] = y[i]/b[i];
    }
    else{
      x[i] = (y[i]-c[i]*x[i+1])/b[i];
    }
  }

  delete[] b;
  delete[] c;
  delete[] y;
  return;
}


void f(double x, double h, double& vector_element){
   vector_element = 100*exp(-10*x)*h;
   return;
}


void closed_form_solution(double x, double& DE_solution){
  DE_solution = 1 - (1 - exp(-10))*x - exp(-10*x);
  return;
}

void compute_errors(double* errors, double* v, double* DE_solution, int n){
  for (int i = 0; i < n; i++){
    errors[i] = log10(abs((v[i] - DE_solution[i])/DE_solution[i]));
  }
  return;
}
