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
| $Q_i$     | quarto $i$ |
| $K_i$     | quarto de casal $i$ |
| $CAPACIDADE_j$ | constante da capacidade de um quarto $j$ |
| $CUSTO_j$ | constante do custo de um quarto $j$ |
| $H_i Q_j$ | hóspede $i$ no quarto $j$
| $C$ | um hóspede que pertence a um casal |
| $Cx_z$, $Cy_z$ | hospede $x$ e seu par $y$, que são um casal $z$ |
| $S_z$ | hospede solteiro que nao pertence a um casal |
| $A_{ij}$ | Antipatia de um hospede $i$ e hospede $j$ no mesmo quarto |
| $ANTIPATIA_{ij}$ | Constante que representa o quanto um hospede $i$ e hospede $j$ não querem ficar no mesmo quarto |

## Minimização

- **Minimizar o custo dos quartos alugados**
```math
min:  
\left( \sum_{j=1}^{q} CUSTO_j * Q_j \right)
```

- **Minimizar a antipatia entre os hóspedes**
```math
min:
\left( \sum_{i=1}^{h} \sum_{j=1}^{h} ANTIPATIA_{ij} * A_{ij} \right)
```

- **Minimizar o custo dos quartos e a antipatia entre os hóspedes**
```math
min: \left( \sum_{j=1}^{q} CUSTO_j * Q_j \right) + \left( \sum_{i=1}^{h} \sum_{j=1}^{h} ANTIPATIA_{ij} * A_{ij} \right)
```

## Cláusuras

### Base
1. **Todos os hóspedes devem estar em somente um quarto**

```math
\forall i \in [1,h]
\left ( \sum_{j=1}^{q} H_iQ_j = 1 \right )
```

2. **A quantidade de hóspede em um quarto deve ser menor ou igual a capacidade do quarto**

```math
\forall j \in [1,q]
\left ( \sum_{i=1}^{h} H_iQ_j \leq CAPACIDADE_j*Q_j  \right )
```

### Casal
3. **O casal deve estar no mesmo quarto**

```math
\forall z \in [1,c], j [1,q]
```
```math
\left ( Cx_zQ_j = Cy_zQ_j  \right)
```

4. **Apenas casais podem estar em quartos de casal**

```math
\forall j \in [1,k]
\left ( \sum_{i=1}^{\sim c} H_iK_j = 0  \right )
```

### Antipatia 

5. **Pessoas em um mesmo quarto geram uma antipatia**

```math
\forall i \in [1,h], j \in [1,h], z \in [1,q] \mid i \neq j 
```
```math
\left ( H_iQ_z + H_jQ_z \leq A_{ij} + 1  \right)
```

## Cláusuras normalizadas

### Base
1. **Todos os hóspedes devem estar em somente um quarto**

```math
\forall i \in [1,h]
```
```math
\left ( \sum_{j=1}^{q} H_iQ_j \ge 1 \right )
```
```math
\left ( \sum_{j=1}^{q} \bar{H_iQ_j} \ge q - 1 \right )
```


2. **A quantidade de hóspede em um quarto deve ser menor ou igual a capacidade do quarto**
```math
\forall j \in [1,q]
\left ( \sum_{i=1}^{h} (\bar{H_iQ_j}) + CAPACIDADE_j*Q_j \ge h - 1 \right )
```

### Casal
3. **O casal deve estar no mesmo quarto**
```math
\forall z \in [1,c], j [1,q]
```
```math
\left ( Cx_zQ_j + \bar{Cy_zQ_j} \ge 1  \right)
```
```math
\left ( \bar{Cx_zQ_j} + Cy_zQ_j \ge 1  \right)
```

4. **Apenas casais podem estar em quartos de casal**
```math
\forall j \in [1,k]
```
```math
\left ( \sum_{i=1}^{\sim c} H_iK_j > 0  \right )
```
```math
\left ( \sum_{i=1}^{\sim c} \bar{H_iK_j} > \sim c  \right )
```

### Antipatia 

5. **Pessoas em um mesmo quarto geram uma antipatia**
```math
\forall i \in [1,h], j \in [1,h], z \in [1,q] | i \neq j
```
```math
\left ( \bar{H_iQ_z} + \bar{H_jQ_z} + A_{ij} \ge 1  \right)
```
