import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Cria um sistema Fuzzy que recebe como input a diferença dos niveis
e o efeito do ataque e devolve como input a probabilidade de ganhar
'''

def calculate_prob(level_input, effect_input):
    # 1. fazer os universos de discurso:


    ## criar o universo level_diff (diferença de nivel) entre -5 a 5
    level_diff =  ctrl.Antecedent(np.arange(-5,6,1), 'level_diff')

    ## criar o universo attack_effect (efeito do ataque) entre 0 e 2
    attack_effect = ctrl.Antecedent(np.arange(0,2.1, 0.1), 'attack_effect')

    ## criar o universo da probabilidade de ganhar separado por 10%
    win_prob = ctrl.Consequent(np.arange(0,1.1,0.1), 'win_prob')

    # 2. Definir as funcoes de pertença -> usamos trimf pois define por nós de forma triangular

    ## para a diferença de nível:
    ### DESVANTAGEM
    level_diff['desvantagem'] = fuzz.trimf(level_diff.universe, [-5, -5, 0])

    ### IGUALDADE
    level_diff['igual'] = fuzz.trimf(level_diff.universe, [-2,0,2])

    ### VANTAGEM
    level_diff['vantagem'] = fuzz.trimf(level_diff.universe, [0,5,5])

    ##para o ataque:
    ### FRACO
    attack_effect['fraco'] = fuzz.trimf(attack_effect.universe, [0,0,1])

    ### NORMAL
    attack_effect['normal'] = fuzz.trimf(attack_effect.universe, [0.5,1,1.5])

    ### FORTE
    attack_effect['forte'] = fuzz.trimf(attack_effect.universe, [1,2,2])

    ##para a probabilidade de ganhar:
    ### BAIXA
    win_prob['baixa'] = fuzz.trimf(win_prob.universe, [0,0,0.5])

    ### MEDIA
    win_prob['media'] = fuzz.trimf(win_prob.universe, [0.25, 0.5, 0.75])

    ### ALTA
    win_prob['alta'] = fuzz.trimf(win_prob.universe, [0.5,1,1])


    # 3. Regras Fuzzy (Base de Conhecimento)

    ## Regras de Derrota (Probabilidade Baixa)
    ### Se estou em desvantagem E o ataque não ajuda (fraco ou normal)
    rule1 = ctrl.Rule(level_diff['desvantagem'] & (attack_effect['fraco'] | attack_effect['normal']), win_prob['baixa'])

    ### Se estamos iguais, mas o meu ataque é inútil
    rule2 = ctrl.Rule(level_diff['igual'] & attack_effect['fraco'], win_prob['baixa'])

    ## Regras de Equilíbrio (Probabilidade Média)
    ### Tudo perfeitamente igual
    rule3 = ctrl.Rule(level_diff['igual'] & attack_effect['normal'], win_prob['media'])

    ### Compensações: Sou mais fraco de nível, mas compenso com um bom ataque
    rule4 = ctrl.Rule(level_diff['desvantagem'] & attack_effect['forte'], win_prob['media'])

    ### Compensações: Sou mais forte, mas o meu ataque é mau contra o tipo dele
    rule5 = ctrl.Rule(level_diff['vantagem'] & attack_effect['fraco'], win_prob['media'])

    ## Regras de Vitória (Probabilidade Alta)
    ### Se tenho vantagem E o ataque é razoável ou muito bom
    rule6 = ctrl.Rule(level_diff['vantagem'] & (attack_effect['normal'] | attack_effect['forte']), win_prob['alta'])

    ### Se estamos iguais de nível, mas eu tenho a vantagem de tipo
    rule7 = ctrl.Rule(level_diff['igual'] & attack_effect['forte'], win_prob['alta'])


    # 4. Desfuzzificação


    # Criar "Cérebro" que contém todas as nossas regras
    prob_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])

    # Criar o simulador onde vamos injetar os dados reais
    prob_sim = ctrl.ControlSystemSimulation(prob_ctrl)

    # Injetamos os valores que recebemos como argumento na função
    prob_sim.input['level_diff'] = level_input
    prob_sim.input['attack_effect'] = effect_input

    # Mandamos a biblioteca fazer as contas (ativar regras + centroide)
    prob_sim.compute()

    # O resultado final exato (crisp value) está guardado aqui
    resultado = prob_sim.output['win_prob']

    return resultado
    


