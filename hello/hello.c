#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Ask the user for his name
    string name = get_string("What's your name? \n");
    printf("hello, %s\n", name);
}