#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <iostream>


#define N 5


int main() {

  // int price_matrix[N][N] = {{0, 1, 11, 7}, {1, 0, 6, 4}, {11, 6, 0, 2}, {7, 4, 2, 0}};
  // int road_matrix[N][N] = {{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}};

  int price_matrix[N][N] = {{0, 10, 5, 4, 1}, {10, 0, 11, 8, 3}, {5, 11, 0, 7, 1}, {4, 8, 7, 0, 6}, {1, 3, 1, 6, 0}};
  int road_matrix[N][N] = {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}};

  int best_sum = 0;
  int sum = 0;
  int tmp_sum1;
  int tmp_sum2;
  int tmp_sum3;

  int start_city, last_city, current_city, prev_city;

  start_city = 0;
  last_city = N-1;

  // FIND INITIAL BEST SUM
  for (int city = start_city + 1; city <= last_city; city++) {
    best_sum += price_matrix[start_city][city];
    road_matrix[start_city][city] = 1;
  }

  // SHOW CURRENT ROAD MAP IN A MATRIX FORM
  for (int i=0; i<N; i++) {
    for (int j=0; j<N; j++) {
      std::cout << price_matrix[i][j] << " ";
    }
    std::cout<<"\n";
  }
  std::cout << "Best sum: " << best_sum << "\n";

  // START FINDING BETTER ROADS
  current_city = start_city + 1;
  prev_city = start_city;

  while (current_city != last_city) {
    std::cout << "\n\nCurrent city :" << current_city + 1 << "\n";
    for (int city = current_city + 1; city <= last_city; city++) {

      tmp_sum1 = price_matrix[current_city][city]; //1
      tmp_sum2 = price_matrix[prev_city][city]; //5
      tmp_sum3 = price_matrix[prev_city][current_city]; //11
      std::cout << tmp_sum1 << " " << tmp_sum2 << " " << tmp_sum3 << "\n";

      if (tmp_sum1 < tmp_sum2) {
        road_matrix[current_city][city] = 1;
        road_matrix[prev_city][city] = 0;
        std::cout << "Build road1: " << current_city+ 1 << city + 1<< "destroy road: " << prev_city + 1<< city + 1<<"\n";
        best_sum = best_sum + tmp_sum1 - tmp_sum2;
      }
      for (int visited_city=0; visited_city<current_city; visited_city++) {

        if (price_matrix[visited_city][current_city] > price_matrix[visited_city][city] + price_matrix[city][current_city] && road_matrix[visited_city][city] != 0) {
          road_matrix[current_city][city] = 1;
          road_matrix[visited_city][current_city] = 0;
          best_sum = best_sum + price_matrix[current_city][city] - price_matrix[visited_city][current_city];
          std::cout << "Build road2: " << current_city + 1<< city + 1 << "destroy road: " << visited_city + 1<< current_city+ 1 <<"\n";
        }
      }
    }
    for (int i=0; i<N; i++) {
      for (int j=0; j<N; j++) {
        std::cout << road_matrix[i][j] << " ";
      }
      std::cout<<"\n";
    }
    std::cout << "Best sum: " << best_sum << "\n";
    prev_city = current_city;
    current_city += 1;
  }

  return 0;
}
