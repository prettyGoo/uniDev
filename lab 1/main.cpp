
// int x = 10;
// void *pointer = &x;
// int y = *((int *) pointer);

#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define N 2

void* calcSum(void* num) {

  printf("Child thread: calculation\n");

  int n = *(int*)num;

  int *divisorSum = new int;
  *divisorSum = 0;

  for (int i=1; i<=n; i++) {
    if (n % i == 0) {
      *divisorSum += i;
    }
  }

  return (void*)divisorSum;
}


int main()
{

  int num1, num2;

  printf("Input two integers: ");
  scanf("%d %d", &num1, &num2);

  void* num1_voidptr;
  void* num2_voidptr;
  num1_voidptr = &num1;
  num2_voidptr = &num2;


  pthread_t th1, th2;

  pthread_create(&th1, NULL, calcSum, num1_voidptr);
  pthread_create(&th2, NULL, calcSum, num2_voidptr);

  int* result1;
  int* result2;

  int check1 = pthread_join(th1, (void**)&result1);
  int check2 = pthread_join(th2, (void**)&result2);

  if (check1 != 0 || check2 != 0) {
    printf("Result will not be correct because of threads error\n");
    return 0;
  }

  printf("Main Thread: result\n");
  if (num1 == *result2) {
    printf("%d is a sum of %d divisors\n", num1, num2);
  }
  else {
    printf("%d is not a sum of %d divisors\n", num1, num2);
  }

  if (num2 == *result1) {
    printf("%d is a sum of %d divisors\n", num2, num1);
  }
  else {
    printf("%d is not a sum of %d divisors\n", num2, num1);
  }

  delete result1;
  delete result2;

  return 0;
}
