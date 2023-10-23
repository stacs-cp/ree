#include "Main_demorgFromNOTconjunction.h"

static bool match_n0(Morphism *morphism);
static bool match_e0(Morphism *morphism);
static bool match_n1(Morphism *morphism, Edge *host_edge);
static bool match_e2(Morphism *morphism);
static bool match_n3(Morphism *morphism, Edge *host_edge);
static bool match_e1(Morphism *morphism);
static bool match_n2(Morphism *morphism, Edge *host_edge);

bool matchMain_demorgFromNOTconjunction(Morphism *morphism)
{
   if(host->number_of_nodes < 4 || host->number_of_edges < 3) return false;
   if(match_n0(morphism)) return true;
   else
   {
      clearMatched(morphism);
      initialiseMorphism(morphism);
      return false;
   }
}

static bool match_n0(Morphism *morphism)
{
   NodeList *nlistpos = NULL;
   for(Node *host_node; (host_node = yieldNextNode(host, &nlistpos)) != NULL;)
   {
      if(nodeMatched(host_node)) continue;
      if(host_node->label.mark != 0) continue;
      if(nodeOutDegree(host_node) < 1       ||
         ((nodeOutDegree(host_node) + nodeInDegree(host_node)) < 1)) continue;

      HostLabel label = host_node->label;
      bool match = false;
      /* Label Matching */
      int new_assignments = 0;
      do
      {
         /* The rule list does not contain a list variable, so there is no
          * match if the host list has a different length. */
         if(label.length != 1) break;
         HostListItem *item = label.list->first;
         /* Matching rule atom 1. */
         if(item->atom.type != 's') break;
         else if(strcmp(item->atom.str, "NOT~UnaryExpression") != 0) break;
         match = true;
      } while(false);

      if(match)
      {
         addNodeMap(morphism, 0, host_node, new_assignments);
         setNodeMatched(host_node);
         if(match_e0(morphism)) return true;
         else
         {
            removeNodeMap(morphism, 0);
            clearNodeMatched(host_node);
         }
      }
      else removeAssignments(morphism, new_assignments);
   }
   return false;
}

static bool match_e0(Morphism *morphism)
{
   /* Start node is the already-matched node from which the candidate
      edges are drawn. End node may or may not have been matched already. */
   Node *host_node = lookupNode(morphism, 0);
   Node *end_node = lookupNode(morphism, 1);
   if(host_node == NULL) return false;
   EdgeList *elistpos;
   elistpos = NULL;
   for(Edge *host_edge; (host_edge = yieldNextOutEdge(host, host_node, &elistpos)) != NULL;)
   {
      if(edgeMatched(host_edge)) continue;
      if(edgeSource(host_edge) == edgeTarget(host_edge)) continue;
      if(host_edge->label.mark != 0) continue;

      /* If the end node has been matched, check that the edgeTarget of the
       * host edge is the image of the end node. */
      if(end_node != NULL)
      {
         if(edgeTarget(host_edge) != end_node) continue;
      }
      /* Otherwise, the edgeTarget of the host edge should be unmatched. */
      else if(nodeMatched(edgeTarget(host_edge))) continue;
      HostLabel label = host_edge->label;
      bool match = false;
      /* Label Matching */
      int new_assignments = 0;
      do
      {
         /* The rule list does not contain a list variable, so there is no
          * match if the host list has a different length. */
         if(label.length != 1) break;
         HostListItem *item = label.list->first;
         /* Matching rule atom 1. */
         if(item->atom.type != 'i') break;
         else if(item->atom.num != 1) break;
         match = true;
      } while(false);

      if(match)
      {
         addEdgeMap(morphism, 0, host_edge, new_assignments);
         setEdgeMatched(host_edge);
         if(match_n1(morphism, host_edge)) return true;
         else
         {
            removeEdgeMap(morphism, 0);
            clearEdgeMatched(host_edge);
         }
      }
      else removeAssignments(morphism, new_assignments);
   }
   return false;
}

static bool match_n1(Morphism *morphism, Edge *host_edge)
{
   Node *host_node = edgeTarget(host_edge);

   if(nodeMatched(host_node)) return false;
   if(host_node->label.mark != 0) return false;
      if(nodeInDegree(host_node) < 1 || nodeOutDegree(host_node) < 2       ||
         ((nodeOutDegree(host_node) + nodeInDegree(host_node)) != 3)) return false;

   HostLabel label = host_node->label;
   bool match = false;
   /* Label Matching */
   int new_assignments = 0;
   do
   {
      /* The rule list does not contain a list variable, so there is no
       * match if the host list has a different length. */
      if(label.length != 1) break;
      HostListItem *item = label.list->first;
      /* Matching rule atom 1. */
      if(item->atom.type != 's') break;
      else if(strcmp(item->atom.str, "AND~BinaryExpression") != 0) break;
      match = true;
   } while(false);

   if(match)
   {
      addNodeMap(morphism, 1, host_node, new_assignments);
      setNodeMatched(host_node);
      if(match_e2(morphism)) return true;
      else
      {
         removeNodeMap(morphism, 1);
         clearNodeMatched(host_node);
      }
   }
   else removeAssignments(morphism, new_assignments);
   return false;
}

static bool match_e2(Morphism *morphism)
{
   /* Start node is the already-matched node from which the candidate
      edges are drawn. End node may or may not have been matched already. */
   Node *host_node = lookupNode(morphism, 1);
   Node *end_node = lookupNode(morphism, 3);
   if(host_node == NULL) return false;
   EdgeList *elistpos;
   elistpos = NULL;
   for(Edge *host_edge; (host_edge = yieldNextOutEdge(host, host_node, &elistpos)) != NULL;)
   {
      if(edgeMatched(host_edge)) continue;
      if(edgeSource(host_edge) == edgeTarget(host_edge)) continue;
      if(host_edge->label.mark != 0) continue;

      /* If the end node has been matched, check that the edgeTarget of the
       * host edge is the image of the end node. */
      if(end_node != NULL)
      {
         if(edgeTarget(host_edge) != end_node) continue;
      }
      /* Otherwise, the edgeTarget of the host edge should be unmatched. */
      else if(nodeMatched(edgeTarget(host_edge))) continue;
      HostLabel label = host_edge->label;
      bool match = false;
      /* Label Matching */
      int new_assignments = 0;
      do
      {
         /* The rule list does not contain a list variable, so there is no
          * match if the host list has a different length. */
         if(label.length != 1) break;
         HostListItem *item = label.list->first;
         /* Matching rule atom 1. */
         if(item->atom.type != 'i') break;
         else if(item->atom.num != 2) break;
         match = true;
      } while(false);

      if(match)
      {
         addEdgeMap(morphism, 2, host_edge, new_assignments);
         setEdgeMatched(host_edge);
         if(match_n3(morphism, host_edge)) return true;
         else
         {
            removeEdgeMap(morphism, 2);
            clearEdgeMatched(host_edge);
         }
      }
      else removeAssignments(morphism, new_assignments);
   }
   return false;
}

static bool match_n3(Morphism *morphism, Edge *host_edge)
{
   Node *host_node = edgeTarget(host_edge);

   if(nodeMatched(host_node)) return false;
   if(host_node->label.mark != 0) return false;
      if(nodeInDegree(host_node) < 1       ||
         ((nodeOutDegree(host_node) + nodeInDegree(host_node)) < 1)) return false;

   HostLabel label = host_node->label;
   bool match = false;
   /* Label Matching */
   int new_assignments = 0;
   do
   {
      /* The rule list does not contain a list variable, so there is no
       * match if the host list has a different length. */
      if(label.length != 1) break;
      HostListItem *item = label.list->first;
      /* Matching rule atom 1. */
      int result = -1;
      /* Matching string variable 1. */
      if(item->atom.type != 's') break;
      result = addStringAssignment(morphism, 1, item->atom.str);
      if(result >= 0)
      {
         new_assignments += result;
      }
      else break;
      match = true;
   } while(false);

   if(match)
   {
      addNodeMap(morphism, 3, host_node, new_assignments);
      setNodeMatched(host_node);
      if(match_e1(morphism)) return true;
      else
      {
         removeNodeMap(morphism, 3);
         clearNodeMatched(host_node);
      }
   }
   else removeAssignments(morphism, new_assignments);
   return false;
}

static bool match_e1(Morphism *morphism)
{
   /* Start node is the already-matched node from which the candidate
      edges are drawn. End node may or may not have been matched already. */
   Node *host_node = lookupNode(morphism, 1);
   Node *end_node = lookupNode(morphism, 2);
   if(host_node == NULL) return false;
   EdgeList *elistpos;
   elistpos = NULL;
   for(Edge *host_edge; (host_edge = yieldNextOutEdge(host, host_node, &elistpos)) != NULL;)
   {
      if(edgeMatched(host_edge)) continue;
      if(edgeSource(host_edge) == edgeTarget(host_edge)) continue;
      if(host_edge->label.mark != 0) continue;

      /* If the end node has been matched, check that the edgeTarget of the
       * host edge is the image of the end node. */
      if(end_node != NULL)
      {
         if(edgeTarget(host_edge) != end_node) continue;
      }
      /* Otherwise, the edgeTarget of the host edge should be unmatched. */
      else if(nodeMatched(edgeTarget(host_edge))) continue;
      HostLabel label = host_edge->label;
      bool match = false;
      /* Label Matching */
      int new_assignments = 0;
      do
      {
         /* The rule list does not contain a list variable, so there is no
          * match if the host list has a different length. */
         if(label.length != 1) break;
         HostListItem *item = label.list->first;
         /* Matching rule atom 1. */
         if(item->atom.type != 'i') break;
         else if(item->atom.num != 1) break;
         match = true;
      } while(false);

      if(match)
      {
         addEdgeMap(morphism, 1, host_edge, new_assignments);
         setEdgeMatched(host_edge);
         if(match_n2(morphism, host_edge)) return true;
         else
         {
            removeEdgeMap(morphism, 1);
            clearEdgeMatched(host_edge);
         }
      }
      else removeAssignments(morphism, new_assignments);
   }
   return false;
}

static bool match_n2(Morphism *morphism, Edge *host_edge)
{
   Node *host_node = edgeTarget(host_edge);

   if(nodeMatched(host_node)) return false;
   if(host_node->label.mark != 0) return false;
      if(nodeInDegree(host_node) < 1       ||
         ((nodeOutDegree(host_node) + nodeInDegree(host_node)) < 1)) return false;

   HostLabel label = host_node->label;
   bool match = false;
   /* Label Matching */
   int new_assignments = 0;
   do
   {
      /* The rule list does not contain a list variable, so there is no
       * match if the host list has a different length. */
      if(label.length != 1) break;
      HostListItem *item = label.list->first;
      /* Matching rule atom 1. */
      int result = -1;
      /* Matching string variable 0. */
      if(item->atom.type != 's') break;
      result = addStringAssignment(morphism, 0, item->atom.str);
      if(result >= 0)
      {
         new_assignments += result;
      }
      else break;
      match = true;
   } while(false);

   if(match)
   {
      addNodeMap(morphism, 2, host_node, new_assignments);
      setNodeMatched(host_node);
      /* All items matched! */
      return true;
   }
   else removeAssignments(morphism, new_assignments);
   return false;
}

void applyMain_demorgFromNOTconjunction(Morphism *morphism, bool record_changes)
{
   Edge *host_edge = lookupEdge(morphism, 0);
   if(record_changes) pushRemovedEdge(host_edge);
   removeEdge(host, host_edge);

   host_edge = lookupEdge(morphism, 1);
   if(record_changes) pushRemovedEdge(host_edge);
   removeEdge(host, host_edge);

   host_edge = lookupEdge(morphism, 2);
   if(record_changes) pushRemovedEdge(host_edge);
   removeEdge(host, host_edge);

   Node *host_node = lookupNode(morphism, 0);
   HostLabel label_n0 = nodeLabel(host_node);
   HostLabel label;
   unsigned short list_var_length0 = 0;
   unsigned short list_length0 = list_var_length0 + 1;
   HostAtom array0[list_length0];
   int index0 = 0;

   array0[index0].type = 's';
   array0[index0++].str = "OR~BinaryExpression";
   if(list_length0 > 0)
   {
      HostList *list0 = makeHostList(array0, list_length0, false);
      label = makeHostLabel(0, list_length0, list0);
   }
   else label = makeEmptyLabel(0);

   if(equalHostLabels(label_n0, label)) removeHostList(label.list);
   else
   {
      if(record_changes) pushRelabelledNode(host_node, label_n0);
      removeHostList(host_node->label.list);
      relabelNode(host_node, label);
   }
   host_node = lookupNode(morphism, 1);
   if(record_changes)
      pushRemovedNode(host_node);
   removeNode(host, host_node);

   /* Array of host node indices indexed by RHS node index. */
   Node *rhs_node_map[5];

   unsigned short list_var_length1 = 0;
   unsigned short list_length1 = list_var_length1 + 1;
   HostAtom array1[list_length1];
   int index1 = 0;

   array1[index1].type = 's';
   array1[index1++].str = "NOT~UnaryExpression";
   if(list_length1 > 0)
   {
      HostList *list1 = makeHostList(array1, list_length1, false);
      label = makeHostLabel(0, list_length1, list1);
   }
   else label = makeEmptyLabel(0);

   host_node = addNode(host, 0, label);
   rhs_node_map[3] = host_node;
   if(record_changes)
      pushAddedNode(host_node);
   unsigned short list_var_length2 = 0;
   unsigned short list_length2 = list_var_length2 + 1;
   HostAtom array2[list_length2];
   int index2 = 0;

   array2[index2].type = 's';
   array2[index2++].str = "NOT~UnaryExpression";
   if(list_length2 > 0)
   {
      HostList *list2 = makeHostList(array2, list_length2, false);
      label = makeHostLabel(0, list_length2, list2);
   }
   else label = makeEmptyLabel(0);

   host_node = addNode(host, 0, label);
   rhs_node_map[4] = host_node;
   if(record_changes)
      pushAddedNode(host_node);
   Node *source, *target;
   source = lookupNode(morphism, 0);
   target = rhs_node_map[3];
   unsigned short list_var_length3 = 0;
   unsigned short list_length3 = list_var_length3 + 1;
   HostAtom array3[list_length3];
   int index3 = 0;

   array3[index3].type = 'i';
   array3[index3++].num = 1;
   if(list_length3 > 0)
   {
      HostList *list3 = makeHostList(array3, list_length3, false);
      label = makeHostLabel(0, list_length3, list3);
   }
   else label = makeEmptyLabel(0);

   host_edge = addEdge(host, label, source, target);
   /* If the edge array size has not increased after the edge addition, then
      the edge was added to a hole in the array. */
   if(record_changes)
      pushAddedEdge(host_edge);
   source = lookupNode(morphism, 0);
   target = rhs_node_map[4];
   unsigned short list_var_length4 = 0;
   unsigned short list_length4 = list_var_length4 + 1;
   HostAtom array4[list_length4];
   int index4 = 0;

   array4[index4].type = 'i';
   array4[index4++].num = 2;
   if(list_length4 > 0)
   {
      HostList *list4 = makeHostList(array4, list_length4, false);
      label = makeHostLabel(0, list_length4, list4);
   }
   else label = makeEmptyLabel(0);

   host_edge = addEdge(host, label, source, target);
   /* If the edge array size has not increased after the edge addition, then
      the edge was added to a hole in the array. */
   if(record_changes)
      pushAddedEdge(host_edge);
   source = rhs_node_map[3];
   target = lookupNode(morphism, 2);
   unsigned short list_var_length5 = 0;
   unsigned short list_length5 = list_var_length5 + 1;
   HostAtom array5[list_length5];
   int index5 = 0;

   array5[index5].type = 'i';
   array5[index5++].num = 1;
   if(list_length5 > 0)
   {
      HostList *list5 = makeHostList(array5, list_length5, false);
      label = makeHostLabel(0, list_length5, list5);
   }
   else label = makeEmptyLabel(0);

   host_edge = addEdge(host, label, source, target);
   /* If the edge array size has not increased after the edge addition, then
      the edge was added to a hole in the array. */
   if(record_changes)
      pushAddedEdge(host_edge);
   source = rhs_node_map[4];
   target = lookupNode(morphism, 3);
   unsigned short list_var_length6 = 0;
   unsigned short list_length6 = list_var_length6 + 1;
   HostAtom array6[list_length6];
   int index6 = 0;

   array6[index6].type = 'i';
   array6[index6++].num = 1;
   if(list_length6 > 0)
   {
      HostList *list6 = makeHostList(array6, list_length6, false);
      label = makeHostLabel(0, list_length6, list6);
   }
   else label = makeEmptyLabel(0);

   host_edge = addEdge(host, label, source, target);
   /* If the edge array size has not increased after the edge addition, then
      the edge was added to a hole in the array. */
   if(record_changes)
      pushAddedEdge(host_edge);
   /* Reset the morphism. */
   clearMatched(morphism);
   initialiseMorphism(morphism);
}

