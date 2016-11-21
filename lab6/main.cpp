#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <string>

using namespace std;

FILE *fp;
pthread_mutex_t mutex;

pthread_cond_t free_file;
pthread_cond_t taken_file;


void *Writer(void *param)
{
  int data = 0;

  while (1)
  {
    for (int i=0; i < 10; i++)
      data += i;

      std::cout << "Writer is writing\n";
      pthread_mutex_lock(&mutex);
      fp = fopen("database.txt", "w");
      fprintf(fp, "%d\n", data);
      fclose(fp);
      pthread_mutex_unlock(&mutex);
      std::cout << "Writer has finished writing\n";

      pthread_cond_broadcast(&free_file);
      for (int j=0; j<100000000; j++) {
       continue;
      }
    }
  }


void *Reader(void *param)
{
  char data[255];
  while (1)
  {
    pthread_cond_wait(&free_file, &mutex);
    std::cout << "Reader is reading\n";
    fp = fopen("database.txt", "r");
    fscanf(fp, "%s", data);
    printf("%s\n", data);
    fclose(fp);
  }
}

int main()
{
  pthread_mutex_init(&mutex, NULL) ;
  pthread_cond_init(&free_file, NULL) ;

  pthread_t writers[2];
  for (int i=0 ; i<2 ; i++) {
    pthread_create(&writers[i], NULL, Writer, NULL);
  }

  pthread_t readers[3];
  for (int i=0 ; i<3 ; i++) {
    pthread_create(&readers[i], NULL, Reader, NULL);
  }

  Reader(NULL) ;
  return 0;
}
