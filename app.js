// EcoEstoque DWS - interface JavaScript usando Fetch API.
// Funciona com executar_demo.py (JSON) ou executar_real.py (MySQL).
'use strict';

const $ = (selector) => document.querySelector(selector);
const state = {
  usuarios: [], materiais: [], reservas: [], emprestimos: [],
  itensEmprestimos: [], itensReserva: [], categorias: [], localizacoes: [],
  modoDemo: false, loaded: false, errors: []
};

function escapeHtml(v) {
  return String(v ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
function number(v) { return Number(v || 0).toLocaleString('pt-BR'); }
function localIso(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
function addDays(days) {
  const d = new Date(); d.setDate(d.getDate() + days); return localIso(d);
}
function prettyDate(v) {
  if (!v) return '—';
  const raw = String(v).slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(raw)) return escapeHtml(v);
  const [y, m, d] = raw.split('-'); return `${d}/${m}/${y}`;
}
function person(id) {
  return state.usuarios.find(u => Number(u.id_usuario) === Number(id))?.nome_usuario ?? `Usuário #${id}`;
}
function material(id) {
  return state.materiais.find(m => Number(m.id_material) === Number(id))?.nome_material ?? (id ? `Material #${id}` : 'Não detalhado');
}
function statusTag(v) {
  const key = String(v ?? '').toLowerCase();
  if (['devolvido', 'finalizado', 'concluido'].includes(key)) return '<span class="pill done">Devolvido</span>';
  if (['pendente', 'aguardando'].includes(key)) return '<span class="pill pending">Pendente</span>';
  if (['cancelado', 'danificado'].includes(key)) return `<span class="pill off">${escapeHtml(v)}</span>`;
  return `<span class="pill">${escapeHtml(v || 'Ativo')}</span>`;
}
function emptyRow(columns, message) {
  return `<tr><td colspan="${columns}" class="table-empty">${escapeHtml(message)}</td></tr>`;
}
function toast(msg, isError = false) {
  const t = $('#toast'); t.textContent = msg;
  t.classList.toggle('error', isError); t.classList.remove('hidden');
  clearTimeout(toast._timer); toast._timer = setTimeout(() => t.classList.add('hidden'), 4200);
}
async function api(path, {method = 'GET', body} = {}) {
  const response = await fetch(path, {
    method,
    headers: body === undefined ? {} : {'Content-Type': 'application/json'},
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: 'no-store'
  });
  let json;
  try { json = await response.json(); } catch { json = null; }
  if (!response.ok) throw new Error(json?.erro || `Erro HTTP ${response.status}`);
  return json;
}

async function refresh() {
  const endpoints = [
    ['usuarios', '/api/usuarios'], ['materiais', '/api/materiais'],
    ['reservas', '/api/reservas'], ['emprestimos', '/api/emprestimos']
  ];
  state.errors = [];
  try {
    const status = await api('/api/status');
    state.modoDemo = status?.modo === 'demo';
  } catch (e) {
    state.errors.push(`Conexão: ${e.message}`);
  }
  const results = await Promise.allSettled(endpoints.map(e => api(e[1])));
  results.forEach((r, idx) => {
    const key = endpoints[idx][0];
    if (r.status === 'fulfilled' && Array.isArray(r.value)) state[key] = r.value;
    else { state[key] = []; state.errors.push(`${key}: ${r.status === 'rejected' ? r.reason.message : 'formato inválido'}`); }
  });
  const extras = await Promise.allSettled([
    api('/api/itens-emprestimos'), api('/api/itens-reserva'),
    api('/api/categorias'), api('/api/localizacoes')
  ]);
  ['itensEmprestimos', 'itensReserva', 'categorias', 'localizacoes'].forEach((key, i) => {
    state[key] = extras[i].status === 'fulfilled' && Array.isArray(extras[i].value) ? extras[i].value : [];
  });
  state.loaded = true;
  const healthy = state.errors.length === 0;
  $('#connection-status').textContent = state.modoDemo ? 'Demonstração local' : healthy ? 'API conectada' : 'API com pendências';
  $('.online-dot').classList.toggle('ok', healthy);
  $('#demo-notice').classList.toggle('hidden', !state.modoDemo);
  $('#alert-bar').classList.toggle('hidden', healthy);
  $('#alert-bar').textContent = healthy ? '' : `Alguns dados não puderam ser carregados (${state.errors.join('; ')}). Sem MySQL, inicie pelo executar_demo.py.`;
  $('#updated-at').textContent = `Atualizado às ${new Date().toLocaleTimeString('pt-BR', {hour:'2-digit', minute:'2-digit'})}`;
  render();
}
function loanItem(loan) {
  return state.itensEmprestimos.find(i => Number(i.id_emprestimo) === Number(loan.id_emprestimo)) || loan.item || null;
}
function reservationItem(reservation) {
  return state.itensReserva.find(i => Number(i.id_reserva) === Number(reservation.id_reserva)) || reservation.item || null;
}
function render() {
  const activeLoans = state.emprestimos.filter(e => !e.data_devolucao).length;
  $('#stat-materiais').textContent = number(state.materiais.length);
  $('#stat-unidades').textContent = number(state.materiais.reduce((a,m) => a + Number(m.qtd_disponivel || 0), 0));
  $('#stat-emprestimos').textContent = number(activeLoans);
  $('#stat-reservas').textContent = number(state.reservas.filter(r => r.status_reserva === 'pendente').length);
  renderFeatured(); renderRecent(); renderMaterials(); renderUsers(); renderReservations(); renderLoans();
}
function renderFeatured() {
  const materials = [...state.materiais].sort((a,b) => Number(b.qtd_disponivel) - Number(a.qtd_disponivel)).slice(0,5);
  $('#featured-materials').innerHTML = materials.length ? materials.map(m => {
    const pct = Math.max(0, Math.min(100, Number(m.qtd_total) ? 100 * m.qtd_disponivel / m.qtd_total : 0));
    return `<div class="featured-row"><div class="material-icon">▣</div><div class="material-name"><strong>${escapeHtml(m.nome_material)}</strong><span>Código #${escapeHtml(m.id_material)}</span></div><div class="stock-qty">${number(m.qtd_disponivel)} / ${number(m.qtd_total)}<div class="progress"><span class="${pct <= 25 ? 'low' : ''}" style="width:${pct}%"></span></div></div></div>`;
  }).join('') : '<div class="empty">Nenhum material cadastrado.</div>';
}
function renderRecent() {
  const loans = [...state.emprestimos].sort((a,b) => Number(b.id_emprestimo) - Number(a.id_emprestimo)).slice(0,5);
  $('#recent-loans').innerHTML = loans.length ? loans.map(e => {
    const item = loanItem(e);
    return `<div class="recent-row"><div class="recent-icon">⇄</div><div class="recent-info"><strong>${escapeHtml(person(e.id_usuario_solicitante))}</strong><span>${escapeHtml(material(item?.id_material))} · ${prettyDate(e.data_retirada)}</span></div>${statusTag(e.data_devolucao ? 'devolvido' : 'emprestado')}</div>`;
  }).join('') : '<div class="empty">Nenhum empréstimo registrado.</div>';
}
function renderMaterials() {
  const q = $('#search-materiais').value.trim().toLowerCase();
  const matches = state.materiais.filter(m => `${m.nome_material} ${m.id_material}`.toLowerCase().includes(q));
  $('#materiais-count').textContent = `${matches.length} material(is)`;
  $('#table-materiais').innerHTML = matches.length ? matches.map(m => {
    const pct = Number(m.qtd_total) ? 100 * Number(m.qtd_disponivel) / Number(m.qtd_total) : 0;
    return `<tr><td><div class="td-identity"><div class="material-icon">▣</div><div><strong>${escapeHtml(m.nome_material)}</strong><div class="small">ID #${escapeHtml(m.id_material)}</div></div></div></td><td>${number(m.qtd_total)}</td><td><strong>${number(m.qtd_disponivel)}</strong></td><td>${m.qtd_disponivel <= 0 ? '<span class="pill off">Indisponível</span>' : pct <= 25 ? '<span class="pill pending">Estoque baixo</span>' : '<span class="pill">Disponível</span>'}</td></tr>`;
  }).join('') : emptyRow(4, 'Nenhum material encontrado.');
}
function renderUsers() {
  const q = $('#search-usuarios').value.trim().toLowerCase();
  const matches = state.usuarios.filter(u => `${u.nome_usuario} ${u.matricula} ${u.tipo_usuario}`.toLowerCase().includes(q));
  $('#usuarios-count').textContent = `${matches.length} usuário(s)`;
  $('#table-usuarios').innerHTML = matches.length ? matches.map(u => `<tr><td><div class="td-identity"><div class="mini-avatar">${escapeHtml((u.nome_usuario || '?').trim().slice(0,2).toUpperCase())}</div><div><strong>${escapeHtml(u.nome_usuario)}</strong><div class="small">ID #${escapeHtml(u.id_usuario)}</div></div></div></td><td>${escapeHtml(u.tipo_usuario)}</td><td>${escapeHtml(u.matricula || '—')}</td><td>${escapeHtml(u.email || '—')}</td></tr>`).join('') : emptyRow(4, 'Nenhum usuário encontrado.');
}
function renderReservations() {
  const rows = [...state.reservas].sort((a,b) => Number(b.id_reserva) - Number(a.id_reserva));
  $('#table-reservas').innerHTML = rows.length ? rows.map(r => {
    const item = reservationItem(r);
    return `<tr><td><span class="tag-id">#${escapeHtml(r.id_reserva)}</span></td><td><strong>${escapeHtml(person(r.id_usuario))}</strong></td><td>${escapeHtml(material(item?.id_material))}${item ? ` <span class="small">· ${escapeHtml(item.qtd_reserva)} un.</span>` : ''}</td><td>${prettyDate(r.data_previsao_retirada)}</td><td>${statusTag(r.status_reserva)}</td></tr>`;
  }).join('') : emptyRow(5, 'Nenhuma reserva encontrada.');
}
function renderLoans() {
  const rows = [...state.emprestimos].sort((a,b) => Number(b.id_emprestimo) - Number(a.id_emprestimo));
  $('#table-emprestimos').innerHTML = rows.length ? rows.map(e => {
    const item = loanItem(e); const active = !e.data_devolucao;
    return `<tr><td><span class="tag-id">#${escapeHtml(e.id_emprestimo)}</span></td><td><strong>${escapeHtml(person(e.id_usuario_solicitante))}</strong></td><td>${escapeHtml(material(item?.id_material))}${item ? ` <span class="small">· ${escapeHtml(item.quantidade_emprestada)} un. · item #${escapeHtml(item.id_item_emprestimo)}</span>` : ''}</td><td>${prettyDate(e.data_previsao_devolucao)}</td><td>${statusTag(active ? 'emprestado' : 'devolvido')}</td><td>${active && item?.id_item_emprestimo ? `<button type="button" class="btn-mini" data-return-item="${Number(item.id_item_emprestimo)}">Devolver</button>` : '<span class="small">—</span>'}</td></tr>`;
  }).join('') : emptyRow(6, 'Nenhum empréstimo cadastrado.');
}

function selectOptions(list, idKey, nameKey) {
  return `<option value="">Selecione...</option>${list.map(i => `<option value="${Number(i[idKey])}">${escapeHtml(i[nameKey])} (#${Number(i[idKey])})</option>`).join('')}`;
}
const userSelect = () => selectOptions(state.usuarios, 'id_usuario', 'nome_usuario');
const materialSelect = () => selectOptions(state.materiais.filter(m=>Number(m.qtd_disponivel)>0), 'id_material', 'nome_material');
const field = (name, label, type='text', opts='') => `<div class="field"><label for="f-${name}">${label}</label><input id="f-${name}" name="${name}" type="${type}" ${opts}></div>`;
const select = (name, label, options) => `<div class="field"><label for="f-${name}">${label}</label><select id="f-${name}" name="${name}" required>${options}</select></div>`;
function openForm(action, itemId = null) {
  const titles = {'novo-usuario':'Cadastrar usuário','novo-material':'Cadastrar material','nova-reserva':'Nova reserva','novo-emprestimo':'Novo empréstimo','nova-devolucao':'Registrar devolução'};
  $('#modal-title').textContent = titles[action] || 'Novo registro';
  let html = '';
  switch(action) {
    case 'novo-usuario':
      html = field('nome_usuario','Nome completo','text','required maxlength="150" placeholder="Ex.: Ana Oliveira"') +
        select('tipo_usuario','Tipo de usuário','<option value="aluno">Aluno</option><option value="professor">Professor</option><option value="admin">Administrador</option>') +
        field('matricula','Matrícula (opcional)','text','maxlength="50" placeholder="Ex.: 2026001"') +
        field('email','E-mail (opcional)','email','maxlength="150" placeholder="Ex.: aluno@escola.com"');
      break;
    case 'novo-material': {
      const category = state.categorias.length ? select('id_categoria','Categoria',selectOptions(state.categorias,'id_categoria','nome_categoria')) : field('id_categoria','ID da categoria (deve existir no MySQL)','number','required min="1" value="1"');
      const location = state.localizacoes.length ? select('id_localizacao','Localização',selectOptions(state.localizacoes,'id_localizacao','nome_localizacao')) : field('id_localizacao','ID da localização (deve existir no MySQL)','number','required min="1" value="1"');
      html = field('nome_material','Nome do material','text','required maxlength="150" placeholder="Ex.: Kit Arduino Uno"') + `<div class="field-grid">${field('qtd_total','Quantidade total','number','required min="0" value="10"')}${field('qtd_disponivel','Quantidade disponível','number','required min="0" value="10"')}</div>` + `<div class="field-grid">${category}${location}</div>`;
      break;
    }
    case 'nova-reserva':
      html = '<div class="modal-help">A reserva cria uma solicitação pendente, mas não retira unidades do estoque.</div>' + select('id_usuario','Solicitante',userSelect()) + select('id_material','Material',materialSelect()) + field('qtd_reserva','Quantidade','number','required min="1" value="1"') + `<div class="field-grid">${field('data_solicitacao','Data da solicitação','date',`required value="${localIso()}"`)}${field('data_previsao_retirada','Retirada prevista','date',`required value="${addDays(1)}"`)}</div>`;
      break;
    case 'novo-emprestimo':
      html = select('id_usuario_solicitante','Usuário solicitante',userSelect()) + select('id_material','Material disponível',materialSelect()) + field('quantidade_emprestada','Quantidade','number','required min="1" value="1"') + `<div class="field-grid">${field('data_retirada','Data da retirada','date',`required value="${localIso()}"`)}${field('data_previsao_devolucao','Devolver até','date',`required value="${addDays(7)}"`)}</div>`;
      break;
    case 'nova-devolucao':
      html = '<div class="modal-help">Informe o ID do <strong>item emprestado</strong>, não o número do empréstimo. São IDs diferentes.</div>' + field('id_item_emprestimo','ID do item emprestado','number',`required min="1" ${itemId ? `value="${Number(itemId)}"` : 'placeholder="Ex.: 1"'}`) + `<div class="field"><label>Estado do material</label><select name="estado_devolucao" required><option value="bom">Bom estado</option></select></div>`;
      break;
    default: return;
  }
  $('#modal-content').innerHTML = `<form id="record-form" data-kind="${action}">${html}<div class="modal-actions"><button class="btn btn-outline" type="button" id="cancel-form">Cancelar</button><button class="btn btn-primary" type="submit" id="save-form">Confirmar</button></div></form>`;
  $('#cancel-form').addEventListener('click', () => $('#modal').close());
  $('#record-form').addEventListener('submit', submitForm);
  $('#modal').showModal();
}
async function submitForm(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const kind = form.dataset.kind;
  const values = Object.fromEntries(new FormData(form).entries());
  const endpoints = {'novo-usuario':'/api/usuarios','novo-material':'/api/materiais','nova-reserva':'/api/reservas','novo-emprestimo':'/api/emprestimos','nova-devolucao':'/api/devolucoes'};
  const numberFields = ['id_categoria','id_localizacao','id_usuario','id_usuario_solicitante','id_material','qtd_total','qtd_disponivel','qtd_reserva','quantidade_emprestada','id_item_emprestimo'];
  for (const key of numberFields) if (values[key] !== undefined) values[key] = Number(values[key]);
  if (kind === 'novo-material' && values.qtd_disponivel > values.qtd_total) { toast('O disponível não pode ser maior que o total.', true); return; }
  const button = $('#save-form'); button.disabled = true; button.textContent = 'Salvando...';
  try {
    await api(endpoints[kind], {method:'POST',body:values});
    $('#modal').close();
    toast(kind === 'nova-devolucao' ? 'Devolução registrada!' : 'Registro salvo com sucesso!');
    await refresh();
  } catch(e) { toast(e.message, true); }
  finally { button.disabled = false; button.textContent = 'Confirmar'; }
}
function showView(name) {
  document.querySelectorAll('.view').forEach(v=>v.classList.toggle('active',v.id===`view-${name}`));
  document.querySelectorAll('.nav-link').forEach(n=>n.classList.toggle('selected',n.dataset.view===name));
  const labels={painel:'VISÃO GERAL',materiais:'MATERIAIS',usuarios:'USUÁRIOS',reservas:'RESERVAS',emprestimos:'EMPRÉSTIMOS'};
  $('#current-page').textContent=labels[name] || name.toUpperCase();
  window.scrollTo({top:0,behavior:'smooth'});
}
function init() {
  document.body.addEventListener('click', e => {
    const view = e.target.closest('[data-view]');
    if (view) { showView(view.dataset.view); return; }
    const action=e.target.closest('[data-action]');
    if (action) { openForm(action.dataset.action); return; }
    const loan=e.target.closest('[data-return-item]');
    if (loan) openForm('nova-devolucao',loan.dataset.returnItem);
  });
  $('#modal-close').addEventListener('click',()=>$('#modal').close());
  $('#search-materiais').addEventListener('input',renderMaterials);
  $('#search-usuarios').addEventListener('input',renderUsers);
  $('#reset-demo').addEventListener('click',async()=>{
    if(!window.confirm('Reiniciar todos os dados de demonstração?')) return;
    try {await api('/api/demo/reset',{method:'POST',body:{}}); toast('Dados de demonstração restaurados.');await refresh();}
    catch(e){toast(e.message,true);}
  });
  refresh();
}
document.addEventListener('DOMContentLoaded',init);
