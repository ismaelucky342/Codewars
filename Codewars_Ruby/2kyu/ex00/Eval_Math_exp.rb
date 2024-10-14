OP_DICT = {
  '+' => ->(a, b) { a + b },
  '-' => ->(a, b) { a - b },
  '*' => ->(a, b) { a * b },
  '/' => ->(a, b) { a / b }
}

def tokenize(e)
  tokens = []
  st = []
  op = {}
  cl = {}

  i = 0
  while i < e.length
    if e[i] == ' '
      i += 1
      next
    end

    if e[i] =~ /\d/
      j = i
      while i + 1 < e.length && (e[i + 1] =~ /\d/ || e[i + 1] == '.')
        i += 1
      end
      tokens << e[j..i].to_f
    else
      if e[i] == '('
        st << tokens.length
      end
      if e[i] == ')'
        j = tokens.length
        op[j] = st.pop
        cl[op[j]] = j
      end
      tokens << e[i]
    end
    i += 1
  end

  [tokens, op, cl]
end

def calc(e)
  tokens, op, cl = tokenize(e)

  eval_muldiv = lambda do |tokens|
    v, o = 1, '*'
    tokens.each do |token|
      if token.is_a?(Float)
        v = OP_DICT[o].call(v, token)
      else
        o = token
      end
    end
    v
  end

  dfs = lambda do |idx_st, idx_en|
    idx = idx_st
    tokens_no_par = []

    while idx <= idx_en
      if tokens[idx] == '('
        v = dfs.call(idx + 1, cl[idx] - 1)
        tokens_no_par << v
        idx = cl[idx]
      else
        tokens_no_par << tokens[idx]
      end
      idx += 1
    end

    tokens_no_neg = []
    idx = 0
    while idx < tokens_no_par.length
      if tokens_no_par[idx] != '-'
        tokens_no_neg << tokens_no_par[idx]
      else
        if idx > 0 && tokens_no_par[idx - 1].is_a?(Float)
          tokens_no_neg << '-'
        else
          j = idx
          while !tokens_no_par[idx].is_a?(Float)
            idx += 1
          end
          n_neg = idx - j
          v = tokens_no_par[idx] * ((-1) ** (n_neg % 2))
          tokens_no_neg << v
        end
      end
      idx += 1
    end

    idx_addsub = [-1]
    tokens_no_neg.each_with_index do |token, idx|
      if token == '+' || token == '-'
        idx_addsub << idx
      end
    end

    v, o = 0, '+'
    (1...idx_addsub.length).each do |i|
      j, k = idx_addsub[i - 1], idx_addsub[i]
      v1 = eval_muldiv.call(tokens_no_neg[(j + 1)...k])
      v = OP_DICT[o].call(v, v1)
      o = tokens_no_neg[k]
    end

    v = OP_DICT[o].call(v, eval_muldiv.call(tokens_no_neg[(idx_addsub[-1] + 1)..-1]))
    v
  end

  dfs.call(0, tokens.length - 1)
end