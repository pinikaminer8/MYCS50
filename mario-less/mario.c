#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Prompt user for height
    int height;
    do
    {
        height = get_int("Waht's the height? \n");
    }
    while (height < 1 || height > 8);

    //Make the pyramid
    for (int i = 1; i <= height; i++)
    {
        for (int k = 1; k <= height - i; k++)
        {
            printf("%c", ' ');
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }


}