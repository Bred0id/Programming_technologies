#ifndef SPLAY_TREE_HPP
#define SPLAY_TREE_HPP

#include <utility>

struct Node {
  int value = 0;
  Node* parent = nullptr;
  Node* left = nullptr;
  Node* right = nullptr;
};

struct SplayTree {
  Node* root = nullptr;

  void SmallRightTurn(Node* node);
  void SmallLeftTurn(Node* node);
  void Splay(Node* node);
  std::pair<Node*, Node*> Split(Node* tree, int key);
  Node* Merge(Node* left, Node* right);
  void Add(int value);
  bool Remove(int value);
  bool Find(int value);
  void Clear(Node* node);
  ~SplayTree();
};

#endif  // SPLAY_TREE_HPP