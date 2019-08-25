#include <iostream>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include "time.h"
#include <armadillo>

using namespace std;
using namespace arma;

ofstream ofile; //Global variable for the output file.

double f(double);   //Declaration of RHS of the differential eq.

int main(int argc, char* argv[]){
  int n = atoi(argv[1]);        //Number of grid points.
  char* outfilename = argv[2];  //Name of the output file.
  double h = 1/((double) n);      //stepsize
  mat A = mat(n,n);   //Creates a (n x n)-matrix.
  clock_t start, finish;  //Declaration of time-storing variables.


  //Fill the matrix with the correct values at its tridiagonal.
  for (int i = 0; i < n; i++){
    if (i < n-1){
      A(i,i) = 2.0;
      A(i,i+1) = -1.0;
      A(i+1,i) = -1.0;
    }
    else{
      A(i,i) = 2.0;
    }
  }
  //A.print("A = ");      //Prints the matrix using armadillos built-in print function.

  //Fill RHS vector q with the correct function values q_i = f(x_i)*h^2
  vec q = vec(n);   //To represent the right hand side.
  double h_squared = h*h;     //Factor to reduce the number of flops in the for-loop.
  for (int i = 0; i < n; i++){
    q(i) = f(i*h)*h_squared;
  }

  start = clock();  //Start of computations.
  //Step 1: Perform LU-decomposition
  mat L, U;           //Empty matrices to be filled using the LU-decomposition function of armadillo
  lu(L,U,A);          //Fills L and U by the rule A = LU.

  //Step 2: Solve Ly = q
  vec y = solve(L,q);     //solves Ly = q using armadillos built-in function "solve".

  //Step 3: Solve Uv = y;
  vec v = solve(U,y);     //Solves Uv = y using armadillos built-in function "solve".

  finish = clock(); //End of computations.
  double timeused = (double) (finish-start)/(CLOCKS_PER_SEC);
  ofile.open(outfilename);
  ofile << timeused << endl;    //Writes the time used on the first line of the output file.

  //Writes the solution vector v to the output file.
  for (int i = 0; i < n; i++){
    ofile << v(i) << endl;
  }
  ofile.close();

  return 0;
}



double f(double x){
  //Specification of the RHS of the differential eq.
  return 100*exp(-10*x);
}
