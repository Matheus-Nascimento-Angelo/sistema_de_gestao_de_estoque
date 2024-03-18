import customtkinter
from os import chdir
from backend import *
from PIL import Image

novo_caminho = "C:\\Users\\Matheus\\Desktop\\projetos_pessoais\\pythonProject1\\interfaces"
chdir(novo_caminho)

app = CTk()
app.geometry("1440x1024")
app.resizable(True, True)
set_appearance_mode("light")

# Login de usuário;
def pag_login():
    main_frame = CTkFrame(master=app,
                          width=427,
                          height=252,
                          fg_color="#EBEBEB"
                          )

    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Input usuário;
    entry_usuario = CTkEntry(master=main_frame,
                             border_color='#7C7C7C',
                             border_width=2,
                             corner_radius=7,
                             placeholder_text="login...",
                             font=('Inter', 17),
                             placeholder_text_color="#BDBDBD",
                             width=427, height=41)

    entry_usuario.place(relx=0.5, rely=0.1, anchor="center")

    # Input senha;
    entry_senha = CTkEntry(master=main_frame,
                           border_color='#7C7C7C',
                           border_width=2,
                           corner_radius=7,
                           placeholder_text="senha...",
                           font=('Inter', 17),
                           placeholder_text_color="#BDBDBD",
                           show="*",
                           width=427, height=41, )

    entry_senha.place(relx=0.5, rely=0.3, anchor="center")

    # Check box Manter Conectado;
    cbox_manter_conectado = CTkCheckBox(master=main_frame,
                                        width=153, height=20,
                                        checkbox_width=16, checkbox_height=16,
                                        fg_color="#00A3FF",
                                        hover_color="#C1C1C1",
                                        border_color="#00A3FF",
                                        border_width=2,
                                        corner_radius=3,
                                        text="Manter conectado", text_color="#000000", font=('Inter', 15))

    cbox_manter_conectado.place(relx=0.2, rely=0.45, anchor="center")

    # Botão de login;
    btn_entrar = CTkButton(master=main_frame,
                           text="Entrar", font=("Inter", 18),
                           corner_radius=6,
                           width=306, height=55,
                           fg_color="#00A3FF",
                           hover_color="#5FC5FF",
                           command=lambda: Usuario.loga_usuario(entry_usuario.get(), entry_senha.get()))

    btn_entrar.place(relx=0.5, rely=0.7, anchor="center")

    lb_nao_tem_conta = CTkLabel(master=main_frame,
                                font=("Inter", 15),
                                text="Não tem conta?",
                                text_color="#000000")

    lb_nao_tem_conta.place(relx=0.35, rely=0.9, anchor="center")

    btn_cadastrese = CTkButton(master=main_frame,
                               text="Cadastre-se",
                               text_color="#00A3FF",
                               font=("Inter", 15),
                               fg_color="#EBEBEB",
                               hover_color="#EBEBEB",
                               width=29,
                               cursor="hand2",
                               command=lambda: main_frame.destroy() or pag_de_cadastro()
                               )

    btn_cadastrese.place(relx=0.58, rely=0.9, anchor="center")


def pag_de_cadastro():
    main_frame = CTkFrame(master=app,
                          width=427,
                          height=385,
                          fg_color="#EBEBEB"
                          )

    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    lb_titulo = CTkLabel(master=main_frame,
                         text="Informações de cadastro",
                         font=("Inter", 38),
                         text_color="#929292"
                         )

    entry_login = CTkEntry(master=main_frame,
                           width=427,
                           height=41,
                           placeholder_text="novo login...",
                           font=("inter", 17),
                           placeholder_text_color="#BDBDBD"
                           )

    entry_senha = CTkEntry(master=main_frame,
                           width=427,
                           height=41,
                           placeholder_text="nova senha...",
                           font=("inter", 17),
                           placeholder_text_color="#BDBDBD",
                           show="*"
                           )

    btn_cadastrese = CTkButton(master=main_frame,
                               width=206, height=39,
                               fg_color="#00A3FF",
                               hover_color="#5FC5FF",
                               text="Cadastrar", text_color="white",
                               corner_radius=6,
                               command=lambda: Usuario.cadastra_usuario(entry_login.get(),
                                                                        entry_senha.get()) or main_frame.destroy() or pag_login()
                               )

    btn_cancelar = CTkButton(master=main_frame,
                             width=206, height=39,
                             fg_color="#00A3FF",
                             hover_color="#5FC5FF",
                             text="Cancelar", text_color="white",
                             corner_radius=6,
                             command=lambda: main_frame.destroy() or pag_login()
                             )

    lb_titulo.place(relx=0.5, rely=0.2, anchor="center")
    entry_login.place(relx=0.5, rely=0.52, anchor="center")
    entry_senha.place(relx=0.5, rely=0.65, anchor="center")
    btn_cadastrese.place(relx=0.25, rely=0.9, anchor="center")
    btn_cancelar.place(relx=0.75, rely=0.9, anchor="center")


# Separação de pedidos;
def pag_de_busca(input_externo=None):
    # FRAMES;
    main_frame = CTkFrame(master=app,
                          width=567,
                          height=508,
                          fg_color="#EBEBEB")

    s_frame = customtkinter.CTkScrollableFrame(
        main_frame,
        height=209,
        width=531,
        border_width=4,
        border_color="#D3D5FF",
        corner_radius=11,
        fg_color="#EBEBEB"
    )

    s_frame.pack(pady=40)

    if input_externo is None:
        def handle_item_selection(posicao, item_info):
            pag_de_retirada(posicao, item_info)

        # Funções;
        def adiciona_ao_scroll():

            for widget in s_frame.winfo_children():
                widget.destroy()
            if etr_item.get():
                posicoes = []
                resultado = Posicao.localiza_item(etr_item.get())
                for botao_info in resultado:
                    posicao = {"codigo_posicao": botao_info["posicao"].upper(),
                               "itens": {"codigo": botao_info["codigo"],
                                         "quantidade": botao_info["quantidade"]}}
                    posicoes.append(posicao)
                    btn = CTkButton(master=s_frame,
                                    width=500,
                                    height=39,
                                    fg_color='#00A3FF',
                                    text=f'Posição : {posicao["codigo_posicao"]}\n Código : {posicao["itens"]["codigo"]} | Quantidade : {posicao["itens"]["quantidade"]}',
                                    command=lambda info=botao_info, posicao=posicao: handle_item_selection(
                                        posicao["codigo_posicao"], info) or main_frame.destroy()
                                    )
                    btn.pack(pady=2)

            else:
                adiciona_ao_scroll_pos()

        def adiciona_ao_scroll_pos():
            for widget in s_frame.winfo_children():
                widget.destroy()

            if etr_posicao.get():
                resultado = Posicao.localiza_posicao(etr_posicao.get())

                for item_info in resultado["itens"]:
                    posicao = resultado["posicao"].upper()
                    btn = CTkButton(master=s_frame,
                                    width=500,
                                    height=39,
                                    fg_color='#00A3FF',
                                    text=f'Código : {item_info["codigo"]} | Quantidade : {item_info["quantidade"]}',
                                    command=lambda info=item_info: handle_item_selection(posicao, info) or main_frame.destroy()
                                    )
                    btn.pack(pady=2)

            else:
                adiciona_ao_scroll()

    else:

        if len(input_externo) > 2:
            def handle_item_selection(posicao, item_info):
                pag_de_retirada(posicao, item_info)

            # Funções;
            def adiciona_ao_scroll():

                for widget in s_frame.winfo_children():
                    widget.destroy()
                posicoes = []
                resultado = Posicao.localiza_item(input_externo)

                for botao_info in resultado:
                    posicao = {"codigo_posicao": botao_info["posicao"].upper(),
                               "itens": {"codigo": botao_info["codigo"],
                               "quantidade": botao_info["quantidade"]}}
                    posicoes.append(posicao)
                    
                    btn = CTkButton(master=s_frame,
                                    width=500,
                                    height=39,
                                    fg_color='#00A3FF',
                                    text=f'Posição : {posicao["codigo_posicao"]}\n Código : {posicao["itens"]["codigo"]} | Quantidade : {posicao["itens"]["quantidade"]}',
                                    command=lambda info=botao_info, posicao=posicao: handle_item_selection(
                                        posicao["codigo_posicao"], info) or main_frame.destroy()
                                    )
                    btn.pack(pady=2)

            adiciona_ao_scroll()

        elif len(input_externo) == 2:

            for widget in s_frame.winfo_children():
                widget.destroy()
            resultado = Posicao.localiza_posicao(input_externo)

            for item_info in resultado["itens"]:
                posicao = resultado["posicao"].upper()
                btn = CTkButton(master=s_frame,
                                width=500,
                                height=39,
                                fg_color='#00A3FF',
                                text=f'Código : {item_info["codigo"]} | Quantidade : {item_info["quantidade"]}',
                                command=lambda info=item_info: handle_item_selection(posicao, info) or main_frame.destroy()
                                )
                btn.pack(pady=2)

    # WIDGETS;

    lb_buscar = CTkLabel(master=main_frame,
                         text="Buscar",
                         font=("Inter", 30),
                         text_color="#00A3FF"
                         )

    etr_item = CTkEntry(master=main_frame,
                        width=426,
                        height=41,
                        placeholder_text="buscar por item..."
                        )

    etr_posicao = CTkEntry(master=main_frame,
                           width=426,
                           height=41,
                           placeholder_text="buscar por posição..."
                           )

    btn_buscar = CTkButton(master=main_frame,
                           width=206,
                           height=39,
                           fg_color="#00A3FF",
                           text="Buscar",
                           font=("Inter", 14),
                           text_color="#FFFFFF",
                           command=lambda: adiciona_ao_scroll() or adiciona_ao_scroll_pos()
                           )

    btn_cancelar = CTkButton(master=main_frame,
                             width=206,
                             height=39,
                             fg_color="#00A3FF",
                             text="Cancelar",
                             font=("Inter", 14),
                             text_color="#FFFFFF",
                             command=lambda: main_page() or main_frame.destroy()
                             )

    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # WIDGETS MAIN_FRAME;
    lb_buscar.place(relx=0.5, rely=0.025, anchor="center")
    etr_item.place(relx=0.5, rely=0.2, anchor="center")
    etr_posicao.place(relx=0.5, rely=0.3, anchor="center")
    btn_buscar.place(relx=0.31, rely=0.44, anchor="center")
    btn_cancelar.place(relx=0.697, rely=0.44, anchor="center")
    s_frame.place(relx=0.5, rely=0.76, anchor="center")


def pag_de_retirada(posicao, item_info):
    # FRAMES;
    main_frame = CTkFrame(master=app,
                          width=428,
                          height=318,
                          fg_color='#EBEBEB'
                          )

    ext_frame = CTkFrame(master=main_frame,
                         width=427,
                         height=125,
                         fg_color="#EBEBEB",
                         border_width=4,
                         corner_radius=9,
                         border_color="#D3D5FF")

    int_frame = CTkFrame(master=ext_frame,
                         width=416,
                         height=71,
                         fg_color="#EBEBEB",
                         border_width=2,
                         border_color="#D3D5FF")

    # WIDGETS MAIN FRAME;

    etr_quantidade = CTkEntry(master=main_frame,
                              width=426,
                              height=41,
                              corner_radius=7,
                              placeholder_text="quantidade...",
                              placeholder_text_color="#BDBDBD")

    etr_pedido = CTkEntry(master=main_frame,
                          width=426,
                          height=41,
                          corner_radius=7,
                          placeholder_text="Pedido...",
                          placeholder_text_color="#BDBDBD")

    btn_retirar = CTkButton(master=main_frame,
                            width=206,
                            height=39,
                            fg_color="#00A3FF",
                            text="Retirar",
                            text_color="#FFFFFF",
                            corner_radius=6,
                            command=lambda: Posicao.retira_item(posicao,
                                                                item_info['codigo'],
                                                                etr_quantidade.get(),
                                                                etr_pedido.get()) or main_frame.destroy() or pag_de_busca())

    btn_cancelar = CTkButton(master=main_frame,
                             width=206,
                             height=39,
                             fg_color="#00A3FF",
                             text="Cancelar",
                             text_color="#FFFFFF",
                             corner_radius=6,
                             command=lambda: main_frame.destroy() or pag_de_busca())

    # WIDGETS INTERN FRAME;

    lb_extern_frame = CTkLabel(master=ext_frame,
                               font=("Inter", 18),
                               text=f"{posicao}",
                               text_color="#00A3FF")

    lb_intern_frame = CTkLabel(master=int_frame,
                               font=("Inter", 13),
                               text_color="#B1B4FB",
                               text=f"Código : {item_info['codigo']}\n"
                                    f"Descrição : {item_info['descricao']}\n"
                                    f"Quantidade : {item_info['quantidade']}"
                               )

    # FRAMES.PLACE;
    main_frame.place(relx=0.5, rely=0.47, anchor="center")
    ext_frame.place(relx=0.5, rely=0.2, anchor="center")
    int_frame.place(relx=0.498, rely=0.55, anchor="center")

    # WIDGETS CENTRAL FRAME.PLACE;
    etr_quantidade.place(relx=0.5, rely=0.6, anchor="center")
    etr_pedido.place(relx=0.5, rely=0.75, anchor="center")
    btn_retirar.place(relx=0.25, rely=0.93, anchor="center")
    btn_cancelar.place(relx=0.75, rely=0.93, anchor="center")
    lb_extern_frame.place(relx=0.5, rely=0.15, anchor="center")
    lb_intern_frame.place(relx=0.5, rely=0.5, anchor="center")


# Entrada em NF;
def pag_de_alocagem():
    def alocar_e_limpar_campos():
        Posicao.aloca_item(etr_codigo_item.get(), etr_quantidade.get(), etr_identificador.get(), etr_posicao.get())
        limpar_campos()

    def limpar_campos():
        etr_codigo_item.delete(0, 'end')
        etr_quantidade.delete(0, 'end')
        etr_identificador.delete(0, 'end')
        etr_posicao.delete(0, 'end')

    # FRAMES;
    main_frame = CTkFrame(master=app,
                          width=427,
                          height=379,
                          fg_color="#EBEBEB")

    # WIDGETS MAIN FRAME;

    lb_title = CTkLabel(master=main_frame,
                        text="Alocar itens",
                        font=("Inter", 30),
                        text_color="#00A3FF")

    etr_codigo_item = CTkEntry(master=main_frame,
                               width=426,
                               height=41,
                               corner_radius=7,
                               fg_color="#FFFFFF",
                               placeholder_text="código do item...")

    etr_quantidade = CTkEntry(master=main_frame,
                              width=426,
                              height=41,
                              corner_radius=7,
                              fg_color="#FFFFFF",
                              placeholder_text="quantidade...")

    etr_posicao = CTkEntry(master=main_frame,
                           width=426,
                           height=41,
                           corner_radius=7,
                           fg_color="#FFFFFF",
                           placeholder_text="posição...")

    etr_identificador = CTkEntry(master=main_frame,
                                 width=426,
                                 height=41,
                                 corner_radius=7,
                                 fg_color="#FFFFFF",
                                 placeholder_text="nota fiscal...")

    btn_alocar = CTkButton(master=main_frame,
                           width=206,
                           height=39,
                           fg_color="#00A3FF",
                           text="Alocar",
                           font=("Inter", 14),
                           text_color="#FFFFFF",
                           command=lambda: alocar_e_limpar_campos()
                           )

    btn_cancelar = CTkButton(master=main_frame,
                             width=206,
                             height=39,
                             fg_color="#00A3FF",
                             text="Cancelar",
                             font=("Inter", 14),
                             text_color="#FFFFFF",
                             command=lambda: main_page() or main_frame.destroy()
                             )

    # WIDGETS MAIN FRAME;
    lb_title.place(relx=0.5, rely=0.04, anchor="center")
    etr_codigo_item.place(relx=0.5, rely=0.25, anchor="center")
    etr_quantidade.place(relx=0.5, rely=0.380, anchor="center")
    etr_posicao.place(relx=0.5, rely=0.51, anchor="center")
    etr_identificador.place(relx=0.5, rely=0.638, anchor="center")
    btn_alocar.place(relx=0.247, rely=0.9, anchor="center")
    btn_cancelar.place(relx=0.76, rely=0.9, anchor="center")

    # FRAMES.PLACE;
    main_frame.place(relx=0.5, rely=0.4, anchor="center")


def pag_log():

    # FRAMES;
    main_frame = CTkFrame(master=app,
                          width=567,
                          height=628,
                          fg_color="#EBEBEB",
                          )

    extern_sframe = CTkFrame(master=main_frame,
                             width=566,
                             height=260,
                             border_width=4,
                             border_color="#D3D5FF",
                             fg_color="#FFFFFF",
                             corner_radius=11)

    s_frame = customtkinter.CTkScrollableFrame(extern_sframe,
                                               width=531,
                                               height=200,
                                               fg_color="#FFFFFF",
                                               corner_radius=9)
    s_frame.pack(pady=40)

    # WIDGETS MAIN FRAME;

    etr_posicao = CTkEntry(master=main_frame,
                           width=426,
                           height=41,
                           fg_color="#FFFFFF",
                           placeholder_text="posição...")

    btn_buscar = CTkButton(master=main_frame,
                           width=206,
                           height=39,
                           fg_color="#00A3FF",
                           text="Buscar",
                           font=("Inter", 14),
                           text_color="#FFFFFF",
                           command=lambda: add_to_scroll())

    btn_cancelar = CTkButton(master=main_frame,
                             width=206,
                             height=39,
                             fg_color="#00A3FF",
                             text="Cancelar",
                             font=("Inter", 14),
                             text_color="#FFFFFF",
                             command=lambda:main_page() or main_frame.destroy())

    lb_posicao = CTkLabel(master=main_frame,
                          text=f"{etr_posicao.get()}",
                          text_color="#00A3FF",
                          font=("Inter", 20)
                          )

    # WIDGETS S_FRAME;

    lb_title = CTkLabel(master=main_frame,
                        text="Log Posição",
                        text_color="#00A3FF",
                        font=("Inter", 30))

    lb_codigo = CTkLabel(master=extern_sframe,
                         text="Código",
                         font=("Inter", 15),
                         text_color="#A5A7C5")

    lb_transacao = CTkLabel(master=extern_sframe,
                            text="Transação",
                            font=("Inter", 15),
                            text_color="#A5A7C5")

    lb_quantidade = CTkLabel(master=extern_sframe,
                             text="Quantidade",
                             font=("Inter", 15),
                             text_color="#A5A7C5")

    lb_data = CTkLabel(master=extern_sframe,
                       text="Data",
                       font=("Inter", 15),
                       text_color="#A5A7C5")

    lb_identificador = CTkLabel(master=extern_sframe,
                                text="Identificador",
                                font=("Inter", 15),
                                text_color="#A5A7C5")

    # MÉTODOS;
    def add_to_scroll():

        for widget in s_frame.winfo_children():
            widget.destroy()
        if etr_posicao.get():
            resultado = Posicao.retorna_log_posicao(etr_posicao.get())
            for log in resultado:
                btn = CTkButton(master=s_frame,
                                width=552,
                                height=27,
                                fg_color="#FFFFFF",
                                text=f"{log['codigo']}          "
                                     f"{log['transacao']}          "
                                     f"{log['quantidade']}          "
                                     f"{log['data']}          "
                                     f"{log['identificador']}",
                                text_color="#A5A7C5",
                                border_width=2,
                                border_color="#A5A7C5",
                                font=("Inter", 14),
                                hover_color="#FFFFFF")
                btn.pack(pady=2)

    # WIDGETS.PLACE;
    etr_posicao.place(relx=0.5, rely=0.3, anchor="center")
    btn_buscar.place(relx=0.3, rely=0.38, anchor="center")
    btn_cancelar.place(relx=0.704, rely=0.38, anchor="center")
    lb_title.place(relx=0.5, rely=0.1, anchor="center")
    lb_posicao.place(relx=0.5, rely=0.3, anchor="center")
    lb_codigo.place(relx=0.1, rely=0.08, anchor="center")
    lb_transacao.place(relx=0.288, rely=0.08, anchor="center")
    lb_quantidade.place(relx=0.5, rely=0.08, anchor="center")
    lb_data.place(relx=0.7, rely=0.08, anchor="center")
    lb_identificador.place(relx=0.88, rely=0.08, anchor="center")

    # FRAMES.PLACE;
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    extern_sframe.place(relx=0.5, rely=0.68, anchor="center")
    s_frame.place(relx=0.5, rely=0.558, anchor="center")


def pag_de_registro():
    main_frame = CTkFrame(master=app,
                          width=1044,
                          height=553,
                          fg_color="#EBEBEB")

    center_left_frame = CTkFrame(master=main_frame,
                                 width=484,
                                 height=458,
                                 fg_color="#EBEBEB")

    center_right_frame = CTkFrame(master=main_frame,
                                  width=484,
                                  height=458,
                                  fg_color="#EBEBEB")

    left_top_frame = CTkFrame(master=center_left_frame,
                              width=484,
                              height=189,
                              fg_color="#FFFFFF")

    left_botton_frame = CTkScrollableFrame(master=center_left_frame,
                                           width=460,
                                           height=182,
                                           fg_color="#FFFFFF")

    rigth_top_frame = CTkFrame(master=center_right_frame,
                               width=484,
                               height=189,
                               fg_color="#FFFFFF")

    rigth_botton_frame = CTkScrollableFrame(master=center_right_frame,
                                            width=460,
                                            height=182,
                                            fg_color="#FFFFFF")

    def show_list():
        for widget in left_botton_frame.winfo_children():
            widget.destroy()

        for item in Item.retorna_catalogo_de_itens():
            btn_item = CTkButton(master=left_botton_frame,
                                 width=455,
                                 height=26,
                                 fg_color="#FFFFFF",
                                 border_width=1,
                                 border_color="#BDBEE3",
                                 text=f"Código : {item['codigo']} | Descrição : {item['descricao']}",
                                 text_color="#BDBEE3",
                                 hover_color="#FFFFFF")

            btn_item.pack(pady=2)

        for widget in rigth_botton_frame.winfo_children():
            widget.destroy()

        for position in Posicao.retorna_catalogo_posicoes():
            btn_position = CTkButton(master=rigth_botton_frame,
                                     width=455,
                                     height=26,
                                     fg_color="#FFFFFF",
                                     border_width=1,
                                     border_color="#BDBEE3",
                                     text=f"{position}",
                                     text_color="#BDBEE3",
                                     hover_color="#FFFFFF")
            btn_position.pack(pady=2)

    show_list()

    # WIDGETS LEFT FRAME_C;
    etr_codigo = CTkEntry(master=left_top_frame,
                          width=426,
                          height=41,
                          placeholder_text="código...",
                          text_color="#D3D5FF",
                          border_color="#D3D5FF")

    etr_descricao = CTkEntry(master=left_top_frame,
                             width=426,
                             height=41,
                             placeholder_text="descrição...",
                             text_color="#D3D5FF",
                             border_color="#D3D5FF")

    btn_registrar = CTkButton(master=left_top_frame,
                              width=142,
                              height=39,
                              fg_color="#00A3FF",
                              corner_radius=6,
                              text="Registrar",
                              command=lambda: add_to_scroll(left_botton_frame)
                              )

    btn_cancelar = CTkButton(master=left_top_frame,
                             width=142,
                             height=39,
                             fg_color="#00A3FF",
                             corner_radius=6,
                             text="Cancelar")

    # WIDGETS RIGHT FRAME_C;
    etr_posicao = CTkEntry(master=rigth_top_frame,
                           width=426,
                           height=41,
                           placeholder_text="código...",
                           text_color="#D3D5FF",
                           border_color="#D3D5FF")

    btn_registrar_r = CTkButton(master=rigth_top_frame,
                                width=142,
                                height=39,
                                fg_color="#00A3FF",
                                corner_radius=6,
                                text="Registrar",
                                command=lambda: add_to_scroll(rigth_botton_frame))

    btn_cancelar_r = CTkButton(master=rigth_top_frame,
                               width=142,
                               height=39,
                               fg_color="#00A3FF",
                               corner_radius=6,
                               text="Cancelar")
    # WIDGETS MAIN FRAME;
    lb_title = CTkLabel(master=main_frame,
                        font=("Inter", 32),
                        text="Cadastros",
                        text_color="#00A3FF")

    lb_cadastrar_itens = CTkLabel(master=main_frame,
                                  font=("Inter", 20),
                                  text="Cadastrar itens",
                                  text_color="#00A3FF")

    lb_cadastrar_posicoes = CTkLabel(master=main_frame,
                                     font=("Inter", 20),
                                     text="Cadastrar posições",
                                     text_color="#00A3FF")

    # FUNÇÕES;
    def add_to_scroll(frame):

        if frame == rigth_botton_frame:

            if etr_posicao.get() != "":
                Posicao.cria_posicao(etr_posicao.get())
                for widget in frame.winfo_children():
                    widget.destroy()
                for position in Posicao.retorna_catalogo_posicoes():
                    btn_position = CTkButton(master=frame,
                                             width=455,
                                             height=26,
                                             fg_color="#FFFFFF",
                                             border_width=1,
                                             border_color="#BDBEE3",
                                             text=f"{position}",
                                             text_color="#BDBEE3",
                                             hover_color="#FFFFFF")
                    btn_position.pack(pady=2)
            else:
                messagebox.showerror("Erro!", "Não é possível cadastrar posições sem nome.")

        if frame == left_botton_frame:
            codigo = etr_codigo.get()
            descricao = etr_descricao.get()
            Item.cadastra_item(codigo, descricao)

            for widget in frame.winfo_children():
                widget.destroy()

            for item in Item.retorna_catalogo_de_itens():
                btn_item = CTkButton(master=frame,
                                     width=455,
                                     height=26,
                                     fg_color="#FFFFFF",
                                     border_width=1,
                                     border_color="#BDBEE3",
                                     text=f"Código : {item['codigo']} | Descrição : {item['descricao']}",
                                     text_color="#BDBEE3",
                                     hover_color="#FFFFFF")

                btn_item.pack(pady=2)

    # FRAMES.PLACE;
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    center_left_frame.place(relx=0.233, rely=0.58, anchor="center")
    center_right_frame.place(relx=0.766, rely=0.58, anchor="center")
    left_top_frame.place(relx=0.5, rely=0.206, anchor="center")
    left_botton_frame.place(relx=0.5, rely=0.764, anchor="center")
    rigth_top_frame.place(relx=0.5, rely=0.206, anchor="center")
    rigth_botton_frame.place(relx=0.5, rely=0.764, anchor="center")

    # WIDGETS MAIN FRAME.PLACE;
    lb_title.place(relx=0.5, rely=0.03, anchor="center")
    lb_cadastrar_itens.place(relx=0.23, rely=0.12, anchor="center")
    lb_cadastrar_posicoes.place(relx=0.755, rely=0.12, anchor="center")

    # WIDGETS LEFT CENTRAL FRAME.PLACE;
    etr_codigo.place(relx=0.5, rely=0.25, anchor="center")
    etr_descricao.place(relx=0.5, rely=0.5, anchor="center")
    btn_registrar.place(relx=0.206, rely=0.8, anchor="center")
    btn_cancelar.place(relx=0.792, rely=0.8, anchor="center")

    # WIDGETS RIGHT CENTRAL FRAME.PLACE;
    etr_posicao.place(relx=0.5, rely=0.25, anchor="center")
    btn_registrar_r.place(relx=0.206, rely=0.8, anchor="center")
    btn_cancelar_r.place(relx=0.792, rely=0.8, anchor="center")


def main_page():


    #FRAMES DEF;
    main_frame = CTkFrame(master=app,
                          width=801,
                          height=440,
                          fg_color="#EBEBEB")

    # WIDGETS DEF;

    btn_separar_pedidos = CTkButton(master=main_frame,
                                    width=195,
                                    height=44,
                                    fg_color="#00A3FF",
                                    corner_radius=60,
                                    font=("Inter", 20),
                                    text="Separar Pedido",
                                    command=lambda: pag_de_busca() or main_frame.destroy()
                                    )

    btn_alocar = CTkButton(master=main_frame,
                           width=195,
                           height=44,
                           fg_color="#00A3FF",
                           corner_radius=60,
                           font=("Inter", 20),
                           text="Alocar Item",
                           command=lambda: pag_de_alocagem() or main_frame.destroy()
                           )

    btn_historico = CTkButton(master=main_frame,
                              width=195,
                              height=44,
                              fg_color="#00A3FF",
                              corner_radius=60,
                              font=("Inter", 20),
                              text="Histórico",
                              command=lambda: pag_log() or main_frame.destroy()
                              )

    image_path = "C:\\Users\\Matheus\\Desktop\\projetos_pessoais\\pythonProject1\\interfaces\\search_7.ico"
    image = Image.open(image_path)
    foto = CTkImage(image, size=(25, 25))

    btn_buscar = CTkButton(master=main_frame,
                           width=425,
                           height=50,
                           corner_radius=60,
                           fg_color="#00A3FF",
                           text="Buscar                                                            ",
                           font=("Inter", 20),
                           image=foto,
                           hover_color="#00A3FF",
                           compound="left",
                           command=lambda: pag_de_busca(etr_posicao_item.get()) or main_frame.destroy())

    etr_posicao_item = CTkEntry(master=btn_buscar,
                                width=350,
                                height=38,
                                bg_color="#00A3FF",
                                corner_radius=60,
                                placeholder_text="Posição ou item...",
                                font=("Inter", 15),
                                border_color="#FFFFFF")
    # FRAMES.PLACE;
    main_frame.place(relx=0.5, rely=0.25, anchor="center")

    # WIDGETS.PLACE;
    btn_separar_pedidos.place(relx=0.251, rely=0.05, anchor="center")
    btn_alocar.place(relx=0.504, rely=0.05, anchor="center")
    btn_historico.place(relx=0.755, rely=0.05, anchor="center")
    etr_posicao_item.place(relx=0.64, rely=0.5, anchor="center")
    btn_buscar.place(relx=0.5, rely=0.92, anchor="center")


main_page()
app.mainloop()
