#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <algorithm>
#include <iostream>

#define N 4


int C[N][N] = {0,4,3,2,4,0,1,2,3,1,0,4,2,2,4,0};
int C[N][N] = {0,2,16,3,2,0,50,3,16,50,0,4,3,3,4,0};
int C[5][5] = {0,7,2,1,1,7,0,2,4,8,2,2,0,1,3,1,4,1,0,6,1,8,3,6,0};

void* calcLocalSum(void* road_num) {

  int rnum = *(int*)road_num; //stores current road n;
  int link[N-2]; // -2 for start point and for current point, stores city order

  std::cout << "\nThread " << rnum << "\n";

  //init possible link
  int j=0;
  for (int i=1; i<=N; i++) {
    if (i != rnum) {
      link[j] = i;
      j++;
    }
  }

  //init best road container
  int road_map[N];
  road_map[0] = 0; road_map[1] = rnum;


  int sum;
  int *best_sum = new int;
  *best_sum = 0;

  do {
    sum = C[0][rnum] + C[rnum][link[0]];
    for (int i=0; i<N-3; i++) {
      sum += C[link[i]][link[i+1]];
    }
    if (sum < *best_sum || *best_sum == 0) {
      *best_sum = sum;
      for (int i=2; i<N; i++) {
        road_map[i] = link[i-2];
      }
    }
  } while ( std::next_permutation(link, link+N-2) );


  std::cout << "Best road map: ";
  for (int i; i<N; i++) {
    std:: cout << road_map[i] << " ";
  }
  std::cout << "\nBest local sum " << *best_sum << "\n";

  return (void*)best_sum;
}


int main() {

  printf("Building road\n");

  int tnums = N -1;
  pthread_t threads[tnums]; int number[N] ;

  for (int i = 0; i < tnums; i++) {
    number[i] = i + 1;
    pthread_create(&threads[i], NULL, calcLocalSum, (void *)(number+i)) ;
  }

  int* local_cost;
  int final_cost = 0;
  for (int i = 0; i < tnums; i++) {

    pthread_join(threads[i], (void **)&local_cost);

    if (*local_cost < final_cost || final_cost == 0)
      final_cost = *local_cost;
  }

  printf("\nThe least expensive building cost is %d\n", final_cost);

  return 0;
}
