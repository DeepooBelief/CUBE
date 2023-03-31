#include<stdio.h>
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




void face_rotate_anticlk(int face[9]){
	int temp1  = face[0];
	int temp2  = face[1];
	face[0] = face[2];
	face[1] = face[5];
	face[2] = face[8];
	face[5] = face[7];
	face[8] = face[6];
	face[7] = face[3];
	face[6] = temp1;
	face[3] = temp2;	
}

void face_rotate_clk(char face[9]){
	char temp1  = face[0];
	char temp2  = face[3];
	face[0] = face[6];
	face[3] = face[7];
	face[6] = face[8];
	face[7] = face[5];
	face[8] = face[2];
	face[5] = face[1];
	face[2] = temp1;
	face[1] = temp2;		
}

// print the cube by text
void printcube(char a[6][N*N]){
	char print_order[] = "4215";
	for(int i = 0; i < N; i++){
		printf("         ");
		for(int j = 0; j < N; j++){
			printf(" %d", a[0][i * N + j]);
			//printf(" %c", a[0][i * N + j]);
		}
		printf("\n");
	}
	for(int i = 0; i < N; i++){
		for(int j = 0; j < 4; j++){
			for(int k = 0; k < N; k++){
				printf(" %d", a[print_order[j] - '0'][i * N + k]);
				//printf(" %c", a[print_order[j] - '0'][i * N + k]);
			}
		}
		printf("\n");
	}
	
	for(int i = 0; i < N; i++){
		printf("         ");
		for(int j = 0; j < N; j++){
			printf(" %d", a[3][i * N + j]);
			//printf(" %c", a[3][i * N + j]);
		}
		printf("\n");
	}
	
}
void rotate_U_side_clk(char a[6][N*N]){
	char temp1 = a[4][0];
	char temp2 = a[4][1];
	char temp3 = a[4][2];
	a[4][0] = a[2][0];
	a[4][1] = a[2][1];
	a[4][2] = a[2][2];
	a[2][0] = a[1][0];
	a[2][1] = a[1][1];
	a[2][2] = a[1][2];
	a[1][0] = a[5][0];
	a[1][1] = a[5][1];
	a[1][2] = a[5][2];
	a[5][0] = temp1;
	a[5][1] = temp2;
	a[5][2] = temp3;
}

void rotate_U_side_anticlk(char a[6][N*N]){
	rotate_U_side_clk(a);
	rotate_U_side_clk(a);
	rotate_U_side_clk(a);
}

void rotate_U(char a[6][N*N]){
	face_rotate_clk(a[0]);
	rotate_U_side_clk(a);
}

void rotate_R_side_clk(char a[6][N*N]){
	char temp1 = a[0][2];
	char temp2 = a[0][5];
	char temp3 = a[0][8];
	a[0][2] = a[2][2];
	a[0][5] = a[2][5];
	a[0][8] = a[2][8];
	a[2][2] = a[3][2];
	a[2][5] = a[3][5];
	a[2][8] = a[3][8];
	a[3][2] = a[5][6];
	a[3][5] = a[5][3];
	a[3][8] = a[5][0];
	a[5][6] = temp1;
	a[5][3] = temp2;
	a[5][0] = temp3;
}

void rotate_R_side_anticlk(char a[6][N*N]){
	rotate_R_side_clk(a);
	rotate_R_side_clk(a);
	rotate_R_side_clk(a);
}

void rotate_F_side_clk(char a[6][N*N]){
	char temp1 = a[0][6];
	char temp2 = a[0][7];
	char temp3 = a[0][8];
	a[0][6] = a[4][8];
	a[0][7] = a[4][5];
	a[0][8] = a[4][2];
	a[4][8] = a[3][2];
	a[4][5] = a[3][1];
	a[4][2] = a[3][0];
	a[3][2] = a[1][0];
	a[3][1] = a[1][3];
	a[3][0] = a[1][6];
	a[1][0] = temp1;
	a[1][3] = temp2;
	a[1][6] = temp3;
}

void rotate_F_side_anticlk(char a[6][N*N]){
	rotate_F_side_clk(a);
	rotate_F_side_clk(a);
	rotate_F_side_clk(a);
}

void rotate_D_side_anticlk(char a[6][N*N]){
	char temp1 = a[2][6];
	char temp2 = a[2][7];
	char temp3 = a[2][8];
	a[2][6] = a[1][6];
	a[2][7] = a[1][7];
	a[2][8] = a[1][8];
	a[1][6] = a[5][6];
	a[1][7] = a[5][7];
	a[1][8] = a[5][8];
	a[5][6] = a[4][6];
	a[5][7] = a[4][7];
	a[5][8] = a[4][8];
	a[4][6] = temp1;
	a[4][7] = temp2;
	a[4][8] = temp3;
}

void rotate_D_side_clk(char a[6][N*N]){
	rotate_D_side_anticlk(a);
	rotate_D_side_anticlk(a);
	rotate_D_side_anticlk(a);
}

void rotate_L_side_clk(char a[6][N*N]){
	char temp1 = a[0][0];
	char temp2 = a[0][3];
	char temp3 = a[0][6];
	a[0][0] = a[5][8];
	a[0][3] = a[5][5];
	a[0][6] = a[5][2];
	a[5][2] = a[3][6];
	a[5][5] = a[3][3];
	a[5][8] = a[3][0];
	a[3][6] = a[2][6];
	a[3][3] = a[2][3];
	a[3][0] = a[2][0];
	a[2][0] = temp1;
	a[2][3] = temp2;
	a[2][6] = temp3;
}

void rotate_L_side_anticlk(char a[6][N*N]){
	rotate_L_side_clk(a);
	rotate_L_side_clk(a);
	rotate_L_side_clk(a);
}

void rotate_B_side_clk(char a[6][N*N]){
	char temp1 = a[0][0];
	char temp2 = a[0][1];
	char temp3 = a[0][2];
	a[0][0] = a[1][2];
	a[0][1] = a[1][5];
	a[0][2] = a[1][8];
	a[1][2] = a[3][8];
	a[1][5] = a[3][7];
	a[1][8] = a[3][6];
	a[3][8] = a[4][6];
	a[3][7] = a[4][3];
	a[3][6] = a[4][0];
	a[4][6] = temp1;
	a[4][3] = temp2;
	a[4][0] = temp3;
}

void rotate_B_side_anticlk(char a[6][N*N]){
	rotate_B_side_clk(a);
	rotate_B_side_clk(a);
	rotate_B_side_clk(a);
}



int main(void)
{
	//int rotate[3][3] = {{1,0,0},{0,0,-1},{0,1,0}};
	int k = 0;
	//face_rotate_clk(try1);
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 9; j++){
			cube[i][j] = k++;
			//cube[i][j] = order[i];
		}
	}
	rotate_U(cube);
	printcube(cube);
	return 0;
}




