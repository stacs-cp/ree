#include <time.h>
#include <Judy.h>
#include "common.h"
#include "debug.h"
#include "graph.h"
#include "graphStacks.h"
#include "parser.h"
#include "lexer.c"
#include "morphism.h"

#include "Main_demorgFromNOTconjunction.h"
Morphism *M_Main_demorgFromNOTconjunction = NULL;

static void freeMorphisms(void)
{
   freeMorphism(M_Main_demorgFromNOTconjunction);
}

static void garbageCollect(void)
{
   freeMorphisms();
   freeGraphChangeStack();
   freeGraph(host);
   freeHostListStore();
}

Graph *host = NULL;
Pvoid_t node_map = (Pvoid_t) NULL;

static Graph *buildHostGraph(char *host_file)
{
   yyin = fopen(host_file, "r");
   if(yyin == NULL)
   {
      perror(host_file);
      return NULL;
   }

   host = newGraph();
   setStackGraph(host);
   /* The parser populates the host graph using node_map to add edges with
    * the correct source and target indices. */
   int result = yyparse();
   fclose(yyin);
   yylex_destroy();
   yy_delete_buffer(YY_CURRENT_BUFFER);
   Word_t Rc_word;
   JLFA(Rc_word, node_map);
   if(result == 0) return host;
   else
   {
      freeGraph(host);
      return NULL;
   }
}

bool success = true;

int main(int argc, char **argv)
{
   srand(time(NULL));
   openLogFile("gp2.log");

   if(argc != 2)
   {
      fprintf(stderr, "Error: missing <host-file> argument.\n");
      return 0;
   }

   initialiseHostListStore();
   host = buildHostGraph(argv[1]);
   if(host == NULL)
   {
      fprintf(stderr, "Error parsing host graph file.\n");
      return 0;
   }
   FILE *output_file = fopen("gp2.output", "w");
   if(output_file == NULL)
   {
      perror("gp2.output");
      exit(1);
   }
   M_Main_demorgFromNOTconjunction = makeMorphism(4, 3, 2);

   /* Rule Call */
   if(matchMain_demorgFromNOTconjunction(M_Main_demorgFromNOTconjunction))
   {
      applyMain_demorgFromNOTconjunction(M_Main_demorgFromNOTconjunction, false);
      success = true;
   }
   else
   {
      fprintf(output_file, "No output graph: rule Main_demorgFromNOTconjunction not applicable.\n");
      printf("Output information saved to file gp2.output\n");
      garbageCollect();
      closeLogFile();
      fclose(output_file);
      return 0;
   }
   printGraph(host, output_file);
   garbageCollect();
   closeLogFile();
   printf("Output graph saved to file gp2.output\n");
   fclose(output_file);
   return 0;
}

