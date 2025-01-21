# Criptografia/Descriptografia S-DES em Python


## Visão Geral
Este projeto implementa o Simplified Data Encryption Standard (S-DES) em Python, uma versão simplificada do algoritmo DES. Ele demonstra conceitos básicos de criptografia, incluindo geração de chaves, criptografia e descriptografia de texto de 8 bits usando uma chave de 10 bits.

## Funcionalidades
- **Geração de Chaves**: Gera duas subchaves de 8 bits a partir de uma chave de 10 bits.
- **Criptografia**: Criptografa um texto de 8 bits usando as subchaves geradas.
- **Descriptografia**: Descriptografa o texto cifrado de 8 bits de volta para o texto original.

## Característica
O SDES oferece os seguintes recursos:

1. Simplicidade: SDES é uma versão simplificada do algoritmo DES mais complexo, facilitando sua compreensão e implementação.
2. Tamanho de bloco pequeno: o SDES opera em blocos de dados de 8 bits, permitindo criptografar e descriptografar pequenas quantidades de dados com eficiência.
3. Chave simétrica: o SDES usa a mesma chave para criptografia e descriptografia, simplificando o processo de gerenciamento de chaves.
4. Criptografia Básica: SDES fornece um nível básico de criptografia adequado para aplicações simples e fins educacionais.
5. Leve: o SDES ocupa pouco espaço de código e tem baixos requisitos computacionais, o que o torna adequado para ambientes com recursos limitados.


## Como Funciona

### Geração de Chaves:
- Uma chave de 10 bits é usada para gerar duas subchaves de 8 bits.
- A chave é permutada e dividida em duas partes, cada uma sendo novamente permutada para gerar as subchaves.

### Criptografia/Descriptografia:
- Utiliza a estrutura Feistel com duas rodadas de criptografia/descriptografia.
- Cada rodada envolve expansão e permutação dos dados, operações XOR com as subchaves e substituição usando S-boxes.

### Criptografia
```python
    def encrypt_block(self, block):
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

        permuted = self.permute(block, IP)
        left, right = permuted[:4], permuted[4:]

        # Rodada 1
        f_output = self.f(right, self.K1)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Troca
        left, right = right, left

        # Rodada 2
        f_output = self.f(right, self.K2)
        left = [l ^ f for l, f in zip(left, f_output)]

        combined = left + right
        return self.permute(combined, IP_INV)

```
Este método realiza a criptografia de um bloco de 8 bits. Ele aplica duas rodadas de transformação, usando as subchaves K1 e K2, e retorna o bloco cifrado.

### Decriptografia 
```python
    def decrypt_block(self, block):
        """Descriptografa um bloco de 8 bits."""
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

        # Permutação inicial
        permuted = self.permute(block, IP)
        left, right = permuted[:4], permuted[4:]

        # Rodada 1 (com K2)
        f_output = self.f(right, self.K2)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Troca
        left, right = right, left

        # Rodada 2 (com K1)
        f_output = self.f(right, self.K1)
        left = [l ^ f for l, f in zip(left, f_output)]

        # Combinação e permutação final
        combined = left + right
        return self.permute(combined, IP_INV)

```
Este método reverte a criptografia, aplicando as rodadas de transformação em ordem inversa (usando K2 e K1) para recuperar o bloco original.

## Interface gráfica

![Screenshot from 2025-01-21 07-57-38](https://github.com/user-attachments/assets/07fee303-92b2-4009-9bce-58d22e175598)

## Menção
SDES é baseado no algoritmo Data Encryption Standard (DES) original desenvolvido pela IBM na década de 1970. A versão simplificada e a implementação do código fornecida neste repositório foram desenvolvidas por mim.
