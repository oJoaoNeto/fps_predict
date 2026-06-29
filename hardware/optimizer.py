from decimal import Decimal
from hardware.models import HardwareComponent
from prediction.predictor import predict_fps

class OptimizationError(Exception):
    pass

def find_best_build(budget, resolution='1080p', quality_preset='Medium', priority='balance'):
    """
    Algoritmo Heuristico/Guloso para encontrar a melhor build de PC dentro do orcamento.
    
    Retorna um dicionario com os componentes selecionados e detalhes do custo e performance.
    """
    budget = Decimal(str(budget))
    
    # 1. Buscar todos os componentes ativos do banco
    components = HardwareComponent.objects.filter(is_active=True)
    
    # Agrupar por categoria
    by_cat = {
        'CPU': [],
        'GPU': [],
        'RAM': [],
        'MOBO': [],
        'PSU': [],
        'STORAGE': []
    }
    
    for c in components:
        if c.category in by_cat:
            by_cat[c.category].append(c)
            
    # Validar se temos pecas em todas as categorias
    for cat, items in by_cat.items():
        if not items:
            raise OptimizationError(f"Nenhum componente cadastrado ou ativo na categoria: {cat}")
            
    best_build = None
    best_score = -1.0
    
    # 2. Iterar sobre combinacoes de CPU e GPU (os maiores geradores de desempenho e custo)
    # Ordenar por preco para otimizar a busca
    cpus = sorted(by_cat['CPU'], key=lambda x: x.price)
    gpus = sorted(by_cat['GPU'], key=lambda x: x.price)
    
    for cpu in cpus:
        cpu_socket = cpu.specs.get('socket')
        cpu_tdp = float(cpu.specs.get('tdp', 65))
        
        for gpu in gpus:
            gpu_tdp = float(gpu.specs.get('tdp', 150))
            
            # Custo parcial
            partial_cost = cpu.price + gpu.price
            if partial_cost >= budget:
                continue # Excede o orcamento logo de cara
                
            # 3. Encontrar placa-mae compativel (mesmo socket da CPU) e mais barata
            compatible_mobos = [
                m for m in by_cat['MOBO']
                if m.specs.get('socket') == cpu_socket
            ]
            if not compatible_mobos:
                continue # Nenhuma placa-mae compativel com essa CPU
            mobo = min(compatible_mobos, key=lambda x: x.price)
            
            # 4. Encontrar fonte (PSU) compativel com potencia suficiente e mais barata
            required_wattage = cpu_tdp + gpu_tdp + 150.0
            compatible_psus = [
                p for p in by_cat['PSU']
                if float(p.specs.get('wattage', 400)) >= required_wattage
            ]
            if not compatible_psus:
                continue # Nenhuma fonte com potencia suficiente
            psu = min(compatible_psus, key=lambda x: x.price)
            
            # 5. Encontrar RAM (preferir 16GB se couber no orcamento, senao a mais barata)
            rams = sorted(by_cat['RAM'], key=lambda x: x.price)
            # Tentar achar uma de 16GB
            rams_16gb = [r for r in rams if int(r.specs.get('size_gb', 8)) >= 16]
            
            # 6. Encontrar Storage mais barato
            storages = sorted(by_cat['STORAGE'], key=lambda x: x.price)
            storage = storages[0] # Comeca com o mais barato
            
            # Vamos testar as opcoes de RAM e Storage que caibam no orcamento
            for ram_option in (rams_16gb + rams if rams_16gb else rams):
                # Evitar duplicar testes se rams_16gb ja contem a ram
                
                # Custo total com RAM e Storage iniciais
                total_cost = cpu.price + gpu.price + mobo.price + psu.price + ram_option.price + storage.price
                
                if total_cost > budget:
                    continue # Estourou o orcamento
                    
                # Se sobrar orçamento, podemos tentar um storage melhor (opcional)
                chosen_storage = storage
                for st in storages[1:]:
                    if total_cost - chosen_storage.price + st.price <= budget:
                        chosen_storage = st
                        total_cost = cpu.price + gpu.price + mobo.price + psu.price + ram_option.price + chosen_storage.price
                
                # 7. Calcular FPS estimado para CS:GO com os componentes selecionados
                ram_size = int(ram_option.specs.get('size_gb', 8))
                fps = predict_fps(
                    game_name="CS:GO",
                    cpu_specs=cpu.specs,
                    gpu_specs=gpu.specs,
                    ram_gb=ram_size,
                    resolution=resolution,
                    quality_preset=quality_preset
                )
                
                # 8. Calcular Pontuacao baseada na prioridade
                if priority == 'performance':
                    score = float(fps)
                elif priority == 'cost-benefit':
                    # FPS por real gasto
                    score = float(fps) / float(total_cost) if total_cost > 0 else 0
                else: # balance (equilibrio)
                    # Valoriza desempenho, mas penaliza gastos excessivos perto do limite do orcamento
                    # Score = FPS * (Porcentagem restante do orcamento + 0.5)
                    remaining_ratio = float((budget - total_cost) / budget)
                    score = float(fps) * (remaining_ratio + 0.5)
                
                # Atualizar melhor build encontrada
                if score > best_score:
                    best_score = score
                    best_build = {
                        'cpu': cpu,
                        'gpu': gpu,
                        'motherboard': mobo,
                        'psu': psu,
                        'ram': ram_option,
                        'storage': chosen_storage,
                        'total_cost': total_cost,
                        'fps': fps,
                        'budget_utilization_percent': round(float(total_cost / budget) * 100, 1)
                    }
                    
    if not best_build:
        raise OptimizationError("Nao foi possivel gerar uma build valida que caiba no orcamento informado.")
        
    return best_build
