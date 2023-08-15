#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);



int main(void)
{
    //get input
    string text = get_string("Text: ");

    //count letters, words and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // compute Coleman-Liau index
    float L = ((float)letters / words) * 100;
    float S = ((float)sentences / words) * 100;
    float index = (0.0588 * L) - (0.296 * S) - 15.8;
    int grade = round(index);

    //Checks whether the score is 16 or higher
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    //Checks whether the score is 1 or lower
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

//A function that measures the number of letters
int count_letters(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //checks how many letter
        if ((text[i] >= 97 && text[i] <= 122) || (text[i] >= 65 && text[i] <= 90))
        {
            count++;
        }
    }
    return count;
}

//A function that measures the number of words
int count_words(string text)
{
    int count = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        //checks how many spaces
        if (text[i] == 32)
        {
            count++;
        }
    }
    return count;
}

//A function that measures the number of sentences
int count_sentences(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //checks how many dots or exclamation mark or question Mark
        if ((text[i] == 33) || (text[i] == 46) || (text[i] == 63))
        {
            count++;
        }
    }
    return count;
}