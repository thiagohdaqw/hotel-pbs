# hotel-pbs

| Sigla    | Significado  |
|----------|:-------------:|
| h        | quantidade de hóspedes |
| q        | quantidade de quartos |
| c        | quantidade de casais |
| -c       | quantidade de não casais |
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

- **O total dos custos dos quartos alugados**
```math
CQ = 
\sum_{j=1}^{q} CUSTO_j * Q_j
```

- **O total da antipatia entre os hóspedes**
```math
AH = 
\sum_{i=1}^{h} \sum_{j=1}^{h} ANTIPATIA_{ij} * A_{ij}
```

- **Minimizar o total de custos dos quartos e a antipatia entre os hóspedes**
```math
min: CQ + AH
```

## Cláusuras

### Base
- **Todos os hóspedes devem estar em somente um quarto**
```math
\forall i \in [1,h]
\left ( \sum_{j=1}^{q} H_iQ_j = 1 \right )
```

- **A quantidade de hóspede em um quarto deve ser menor ou igual a capacidade do quarto**
```math
\forall j \in [1,q]
\left ( \sum_{i=1}^{h} H_iQ_j \leq CAPACIDADE_j*Q_j  \right )
```

### Casal
- **O casal deve estar no mesmo quarto**
```math
\forall z \in [1,c], j [1,q]
\left ( Cx_zQ_j = Cy_zQ_j  \right)
```

- **Os casais devem estar em um quarto de casal**
```math
\forall i \in [1,k]
\left ( \sum_{z=1}^{c} C_zK_i \geq 1  \right )
```


- **Apenas casais podem estar em quartos de casal**
```math
\forall j \in [1,k]
\left ( \sum_{i=1}^{-c} H_iK_j = 0  \right )
```

### Antipatia 

- **Pessoas em um mesmo quarto geram uma antipatia**
```math
\forall i \in [1,h], j \in [1,h], z \in [1,q] | i \neq j 
\left ( H_iQ_z + H_jQ_z \leq A_{ij} + 1  \right)
```


## Uso

`python3 -m hotel samples/root.desc`
