// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//number of buckets in hash table
const unsigned int N = 100000;
int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int hashword = hash(word);

    node *marker = table[hashword];

    while(marker != NULL)
    {
        if(strcasecmp(marker->word, word) == 0)
        {
            return true;
        }
        marker = marker->next;
    }

    return false;
}

unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = (hash * 14 + tolower(word[i])) % N;
    }
    return hash;
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *current = fopen(dictionary, "r");

    if(current == NULL)
    {
        return false;
    }
    char word[LENGTH + 1];
    while(fscanf(current, "%s", word) != EOF)
    {
        node *temp = malloc(sizeof(node));

        if (temp == NULL)
        {
            return false;
        }

        strcpy(temp->word, word);

        unsigned int hashword = hash(word);

        if(table[hashword] == NULL)
        {
            temp->next = NULL;
        }
        else
        {
            temp->next = table[hashword];
        }

        table[hashword] = temp;

        counter++;
    }

    fclose(current);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

void free_all(node *n)
{
    if(n->next)
    {
        free_all(n->next);
    }
    free(n);
}


// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(unsigned int i = 0; i < N; i++)
    {
        if(table[i] != NULL)
        {
            free_all(table[i]);
        }
    }
    return true;
}
