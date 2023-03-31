#include<stdio.h>
#include "./cube_move.h"
#define N 3
#define LETTER

char cube[6][N*N] = {};
         
char cube_pos[] = {'U', 'D', 'F', 'B', 'L', 'R'};

char order[] = "URFDLB";
//U,L,F,R,D,B

//int cube[54] = {0};
         
int turn = 0;

void swap(int *a, int *b)
{
	int tmp = *a;
	*a = *b;
	*b = tmp;
	
}
int try1[3][3] = {{1,2,3},{4,5,6},{7,8,9}};

#ifdef LETTER
void printcube(char a[6][N*N]){
	char print_order[] = "4215";
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %c", a[0][i * N + j]);
		}
		printf("\n");
	}
	for(int i = 0; i < N; i++){
		for(int j = 0; j < 4; j++){
			for(int k = 0; k < N; k++){
				printf(" %c", a[print_order[j] - '0'][i * N + k]);
			}
		}
		printf("\n");
	}
	
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %c", a[3][i * N + j]);
		}
		printf("\n");
	}
	
}
#else
// print the cube by text
void printcube(char a[6][N*N]){
	char print_order[] = "4215";
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %d", a[0][i * N + j]);
		}
		printf("\n");
	}
	for(int i = 0; i < N; i++){
		for(int j = 0; j < 4; j++){
			for(int k = 0; k < N; k++){
				printf(" %d", a[print_order[j] - '0'][i * N + k]);
			}
		}
		printf("\n");
	}
	
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %d", a[3][i * N + j]);
		}
		printf("\n");
	}
	
}

#endif

int main(void)
{
	int k = 0;
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 9; j++){
			#ifndef LETTER
			cube[i][j] = k++;
			#else
			cube[i][j] = order[i];
			#endif
		}
	}
	rotate_R(cube);
	rotate_U(cube);
	rotate_R_anti(cube);
	rotate_U(cube);
	rotate_R(cube);
	rotate_U(cube);
	rotate_U(cube);
	rotate_R_anti(cube);
	printcube(cube);
	return 0;
}




