#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    //get text from input
    string text = get_string("Message: ");

    // Get the length of the input string and declare an array of the same length to store ascii
    int text_len = strlen(text);
    int ascii[text_len];

    //convert letters to ascii nums
    for (int i = 0; i < strlen(text); i++)
    {
        ascii[i] = text[i];
    }
    //itirate through all the text
    for (int j = 0; j < strlen(text); j++)
    {
        int bits[8], bit = ascii[j];

        //Convert the ascii value to binary
        for (int i = 7; i > 0; i--)
        {
            bits[i] = bit % 2;
            bit /= 2;
        }

        // Print the binary representation
        for (int i = 0; i < 8; i++)
        {
            int bulb = bits[i];
            print_bulb(bulb);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
