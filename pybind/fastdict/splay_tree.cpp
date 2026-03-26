#include "splay_tree.hpp"

void SplayTree::SmallRightTurn(Node* node) {
  Node* tmp = node->left;
  Node* tmp_right = tmp->right;
  tmp->parent = node->parent;
  if (node->parent == nullptr) {
    root = tmp;
  } else if (node->parent->left == node) {
    node->parent->left = tmp;
  } else {
    node->parent->right = tmp;
  }
  node->left = tmp_right;
  if (tmp_right != nullptr) {
    tmp_right->parent = node;
  }
  tmp->right = node;
  node->parent = tmp;
}

void SplayTree::SmallLeftTurn(Node* node) {
  Node* tmp = node->right;
  Node* tmp_left = tmp->left;
  tmp->parent = node->parent;
  if (node->parent == nullptr) {
    root = tmp;
  } else if (node->parent->left == node) {
    node->parent->left = tmp;
  } else {
    node->parent->right = tmp;
  }
  node->right = tmp_left;
  if (tmp_left != nullptr) {
    tmp_left->parent = node;
  }
  tmp->left = node;
  node->parent = tmp;
}

void SplayTree::Splay(Node* node) {
  while (node->parent != nullptr) {
    if (node->parent->parent == nullptr) {
      if (node->parent->left == node) {
        SmallRightTurn(node->parent);
      } else {
        SmallLeftTurn(node->parent);
      }
    } else if (node->parent->left == node && node->parent->parent->left == node->parent) {
      SmallRightTurn(node->parent->parent);
      SmallRightTurn(node->parent);
    } else if (node->parent->right == node && node->parent->parent->right == node->parent) {
      SmallLeftTurn(node->parent->parent);
      SmallLeftTurn(node->parent);
    } else if (node->parent->left == node && node->parent->parent->right == node->parent) {
      SmallRightTurn(node->parent);
      SmallLeftTurn(node->parent);
    } else {
      SmallLeftTurn(node->parent);
      SmallRightTurn(node->parent);
    }
  }
  root = node;
}

std::pair<Node*, Node*> SplayTree::Split(Node* tree, int key) {
  if (tree == nullptr) {
    return {nullptr, nullptr};
  }
  Node* node = tree;
  Node* last = nullptr;
  while (node != nullptr) {
    last = node;
    if (key < node->value) {
      node = node->left;
    } else if (key > node->value) {
      node = node->right;
    } else {
      Splay(node);
      tree = node;
      break;
    }
  }
  if (node == nullptr && last != nullptr) {
    Splay(last);
    tree = last;
  }
  if (tree->value <= key) {
    Node* right = tree->right;
    if (right != nullptr) {
      right->parent = nullptr;
    }
    tree->right = nullptr;
    return {tree, right};
  }
  Node* left = tree->left;
  if (left != nullptr) {
    left->parent = nullptr;
  }
  tree->left = nullptr;
  return {left, tree};
}

Node* SplayTree::Merge(Node* left, Node* right) {
  if (left == nullptr) {
    return right;
  }
  if (right == nullptr) {
    return left;
  }
  Node* max_left = left;
  while (max_left->right != nullptr) {
    max_left = max_left->right;
  }
  Splay(max_left);
  max_left->right = right;
  if (right != nullptr) {
    right->parent = max_left;
  }
  return max_left;
}

void SplayTree::Add(int value) {
  auto [L, R] = Split(root, value);
  Node* new_node = new Node{value, nullptr, nullptr, nullptr};
  root = Merge(Merge(L, new_node), R);
}

bool SplayTree::Remove(int value) {
  auto [L, R] = Split(root, value - 1);
  auto [M, R2] = Split(R, value);
  if (M == nullptr) {
    root = Merge(L, Merge(M, R2));
    return false;
  }
  Clear(M);
  root = Merge(L, R2);
  return true;
}

bool SplayTree::Find(int value) {
  Node* node = root;
  Node* last = nullptr;
  while (node != nullptr) {
    last = node;
    if (value == node->value) {
      Splay(node);
      return true;
    }
    if (value < node->value) {
      node = node->left;
    } else {
      node = node->right;
    }
  }
  if (last != nullptr) {
    Splay(last);
  }
  return false;
}

void SplayTree::Clear(Node* node) {
  if (node == nullptr) {
    return;
  }
  Clear(node->left);
  Clear(node->right);
  delete node;
}

SplayTree::~SplayTree() {
  Clear(root);
}