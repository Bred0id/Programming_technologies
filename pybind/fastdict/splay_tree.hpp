#ifndef SPLAY_TREE_HPP
#define SPLAY_TREE_HPP

#include <stdexcept>
#include <utility>
#include <vector>

template <class Key, class Value>
class SplayTree {
  struct Node {
    Key key_;
    Value value_;
    Node* parent_ = nullptr;
    Node* left_ = nullptr;
    Node* right_ = nullptr;

    Node() = default;

    Node(const Key& k, const Value& v) : key_(k), value_(v) {
    }

    ~Node() = default;
  };

  Node* root_ = nullptr;
  size_t size_ = 0;

  void SmallRightTurn(Node* node) {
    Node* tmp = node->left_;
    Node* tmp_right = tmp->right_;
    tmp->parent_ = node->parent_;
    if (node->parent_ == nullptr) {
      root_ = tmp;
    } else if (node->parent_->left_ == node) {
      node->parent_->left_ = tmp;
    } else {
      node->parent_->right_ = tmp;
    }
    node->left_ = tmp_right;
    if (tmp_right != nullptr) {
      tmp_right->parent_ = node;
    }
    tmp->right_ = node;
    node->parent_ = tmp;
  }

  void SmallLeftTurn(Node* node) {
    Node* tmp = node->right_;
    Node* tmp_left = tmp->left_;
    tmp->parent_ = node->parent_;
    if (node->parent_ == nullptr) {
      root_ = tmp;
    } else if (node->parent_->left_ == node) {
      node->parent_->left_ = tmp;
    } else {
      node->parent_->right_ = tmp;
    }
    node->right_ = tmp_left;
    if (tmp_left != nullptr) {
      tmp_left->parent_ = node;
    }
    tmp->left_ = node;
    node->parent_ = tmp;
  }

  void Splay(Node* node) {
    while (node->parent_ != nullptr) {
      if (node->parent_->parent_ == nullptr) {
        if (node->parent_->left_ == node) {
          SmallRightTurn(node->parent_);
        } else {
          SmallLeftTurn(node->parent_);
        }
      } else if (node->parent_->left_ == node && node->parent_->parent_->left_ == node->parent_) {
        SmallRightTurn(node->parent_->parent_);
        SmallRightTurn(node->parent_);
      } else if (node->parent_->right_ == node && node->parent_->parent_->right_ == node->parent_) {
        SmallLeftTurn(node->parent_->parent_);
        SmallLeftTurn(node->parent_);
      } else if (node->parent_->left_ == node && node->parent_->parent_->right_ == node->parent_) {
        SmallRightTurn(node->parent_);
        SmallLeftTurn(node->parent_);
      } else {
        SmallLeftTurn(node->parent_);
        SmallRightTurn(node->parent_);
      }
    }
    root_ = node;
  }

  Node* FindNode(const Key& key) {
    Node* node = root_;
    Node* last = nullptr;
    while (node != nullptr) {
      last = node;
      if (node->key_ < key) {
        node = node->right_;
      } else if (key < node->key_) {
        node = node->left_;
      } else {
        Splay(node);
        return node;
      }
    }
    if (last != nullptr) {
      Splay(last);
    }
    return nullptr;
  }

  std::pair<Node*, Node*> Split(const Key& key) {
    if (root_ == nullptr) {
      return {nullptr, nullptr};
    }
    if (!(key < root_->key_)) {
      Node* right = root_->right_;
      if (right != nullptr) {
        right->parent_ = nullptr;
      }
      root_->right_ = nullptr;
      return {root_, right};
    }
    Node* left = root_->left_;
    if (left != nullptr) {
      left->parent_ = nullptr;
    }
    root_->left_ = nullptr;
    return {left, root_};
  }

  Node* Merge(Node* left, Node* right) {
    if (left == nullptr) {
      return right;
    }
    if (right == nullptr) {
      return left;
    }
    root_ = left;
    Node* max_left = left;
    while (max_left->right_ != nullptr) {
      max_left = max_left->right_;
    }
    Splay(max_left);
    max_left->right_ = right;
    right->parent_ = max_left;
    return max_left;
  }

  void InOrder(Node* node, std::vector<Node*>& nodes) const {
    if (node == nullptr) {
      return;
    }
    InOrder(node->left_, nodes);
    nodes.push_back(node);
    InOrder(node->right_, nodes);
  }

  std::vector<Node*> GetNodes() const {
    std::vector<Node*> nodes;
    InOrder(root_, nodes);
    return nodes;
  }

  void Clear(Node* node) {
    if (node == nullptr) {
      return;
    }
    Clear(node->left_);
    Clear(node->right_);
    delete node;
  }

 public:
  size_t Size() const {
    return size_;
  }

  bool Contains(const Key& key) {
    return FindNode(key) != nullptr;
  }

  void Add(const Key& key, const Value& value) {
    if (root_ == nullptr) {
      root_ = new Node(key, value);
      size_++;
      return;
    }
    if (FindNode(key) != nullptr) {
      root_->value_ = value;
      return;
    }
    auto [L, R] = Split(key);
    Node* new_node = new Node(key, value);
    root_ = Merge(Merge(L, new_node), R);
    size_++;
  }

  bool Remove(const Key& key) {
    if (!Contains(key)) {
      return false;
    }
    Node* left = root_->left_;
    Node* right = root_->right_;
    if (left != nullptr) {
      left->parent_ = nullptr;
    }
    if (right != nullptr) {
      right->parent_ = nullptr;
    }
    delete root_;
    root_ = Merge(left, right);
    size_--;
    return true;
  }

  Value& Find(const Key& key) {
    Node* node = FindNode(key);
    if (node == nullptr) {
      throw std::out_of_range("Key not found");
    }
    return node->value_;
  }

  std::vector<Key> GetKeys() const {
    std::vector<Key> keys;
    for (auto* node : GetNodes()) {
      keys.push_back(node->key_);
    }
    return keys;
  }

  std::vector<Value> GetValues() const {
    std::vector<Value> values;
    for (auto* node : GetNodes()) {
      values.push_back(node->value_);
    }
    return values;
  }

  std::vector<std::pair<Key, Value>> GetItems() const {
    std::vector<std::pair<Key, Value>> items;
    for (auto* node : GetNodes()) {
      items.push_back({node->key_, node->value_});
    }
    return items;
  }

  ~SplayTree() {
    Clear(root_);
  }
};

#endif