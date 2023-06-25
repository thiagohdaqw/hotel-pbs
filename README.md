# hotel-pbs

## Uso
```bash
$ export PATH=$PATH:<path_to_clasp_bin_folder>
$ export DEBUG=1
$ python3 -m hotel samples/root.desc
```

## Formulas

| Sigla    | Significado  |
|----------|:-------------:|
| h        | quantidade de hóspedes |
| q        | quantidade de quartos |
| c        | quantidade de casais |
| $\sim c$       | quantidade de não casais |
| k         | quantidade de quartos de casal |
| $q_i$     | quarto $i$ |
| $k_i$     | quarto de casal $i$ |
| $CAPACIDADE_j$ | constante da capacidade de um quarto $j$ |
| $CUSTO_j$ | constante do custo de um quarto $j$ |
| $h_iq_j$ | hóspede $i$ no quarto $j$
| $cx_z$, $cy_z$ | hospede $x$ e seu par $y$, que são um casal $z$ |
| $a_{ij}$ | Antipatia de um hospede $i$ e hospede $j$ no mesmo quarto |
| $ANTIPATIA_{ij}$ | Constante que representa o quanto um hospede $i$ e hospede $j$ não querem ficar no mesmo quarto |

## Minimização

- **Minimizar o custo dos quartos alugados**
```math
min:  
\left( \sum_{j=1}^{q} CUSTO_j . q_j \right)
```

- **Minimizar a antipatia entre os hóspedes**
```math
min:
\left( \sum_{i,j = {h \choose 2}} ANTIPATIA_{ij} . a_{ij} \right)
```

- **Minimizar o custo dos quartos e a antipatia entre os hóspedes**
```math
min: \left( \sum_{j=1}^{q} CUSTO_j . q_j \right) + \left( \sum_{i,j = {h \choose 2}} ANTIPATIA_{ij} . a_{ij} \right)
```

## Cláusuras

### Base
1. **Todos os hóspedes devem estar em somente um quarto**

```math
\forall i \in [1,h]
\left ( \sum_{j=1}^{q} h_iq_j = 1 \right )
```

2. **A quantidade de hóspede em um quarto deve ser menor ou igual a capacidade do quarto**

```math
\forall j \in [1,q]
\left ( \sum_{i=1}^{h} h_iq_j \leq CAPACIDADE_j . q_j  \right )
```

### Casal
3. **O casal deve estar no mesmo quarto**

```math
\forall z \in [1,c], j [1,q]
```
```math
\left ( cx_zq_j = cy_zq_j  \right)
```

4. **Apenas casais podem estar em quartos de casal**

```math
\forall j \in [1,k]
\left ( \sum_{i=1}^{\sim c} h_ik_j = 0  \right )
```

### Antipatia 

5. **Pessoas em um mesmo quarto geram uma antipatia**

```math
\forall i,j \in {h \choose 2}, z \in [1,q]
```
```math
\left ( h_iq_z + h_jq_z \leq a_{ij} + 1  \right)
```

## Cláusuras normalizadas

### Base
1. **Todos os hóspedes devem estar em somente um quarto**

```math
\forall i \in [1,h]
```
```math
\left ( \sum_{j=1}^{q} h_iq_j \ge 1 \right )
```
```math
\left ( \sum_{j=1}^{q} \bar{h_iq_j} \ge q - 1 \right )
```


2. **A quantidade de hóspede em um quarto deve ser menor ou igual a capacidade do quarto**
```math
\forall j \in [1,q]
\left ( \sum_{i=1}^{h} (\bar{h_iq_j}) + CAPACIDADE_j*q_j \ge h \right )
```

### Casal
3. **O casal deve estar no mesmo quarto**
```math
\forall z \in [1,c], j [1,q]
```
```math
\left ( cx_zq_j + \bar{cy_zq_j} \ge 1  \right)
```
```math
\left ( \bar{cx_zq_j} + cy_zq_j \ge 1  \right)
```

4. **Apenas casais podem estar em quartos de casal**
```math
\forall j \in [1,k]
```
```math
\left ( \sum_{i=1}^{\sim c} h_ik_j > 0  \right )
```
```math
\left ( \sum_{i=1}^{\sim c} \bar{h_ik_j} > \sim c  \right )
```

### Antipatia 

5. **Pessoas em um mesmo quarto geram uma antipatia**
```math
\forall i,j \in {h \choose 2}, z \in [1,q]
```
```math
\left ( \bar{h_iq_z} + \bar{h_jq_z} + a_{ij} \ge 1  \right)
```
