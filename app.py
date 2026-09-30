import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("transacoes.csv", encoding="latin1")
df_cotacoes = pd.read_csv("cotacoes.csv", encoding="utf-8")

df = df.drop_duplicates(keep="first")
mediana_estado = df.groupby("estado_cliente")["valor"].transform("median")
df["valor"] = df["valor"].fillna(mediana_estado)
df["data_transacao"] = pd.to_datetime(df["data_transacao"])
df["data_transacao"] = df["data_transacao"].dt.tz_localize("America/Sao_Paulo")
df["plataforma"] = "Mobile"
df["dia_semana"] = df["data_transacao"].dt.day_name()
df["mes"] = df["data_transacao"].dt.month

risco_dict = {
    "C100": "Baixo",
    "C101": "Alto",
    "C102": "Médio",
    "C103": "Médio",
    "C104": "Baixo",
}
df["nivel_risco"] = df["id_cliente"].map(risco_dict)

filtro_setembro = (
    (df["mes"] == 9)
    & ((df["estado_cliente"] == "SP") | (df["estado_cliente"] == "RJ"))
    & (df["valor"] > 5000)
)
df_setembro = df[filtro_setembro]

tabela_risco = pd.pivot_table(
    df,
    index="mes",
    columns="nivel_risco",
    values="valor",
    aggfunc="sum",
    margins=True,
)

media_estado = df.groupby("estado_cliente")["valor"].transform("mean")
desvio_estado = df.groupby("estado_cliente")["valor"].transform("std")
df["z_score"] = (df["valor"] - media_estado) / desvio_estado
df_anomalias = df[df["z_score"] > 2.5]

totais_diarios = df.set_index("data_transacao")["valor"].resample("D").sum()
media_movel = totais_diarios.rolling(7).mean()

df_cotacoes["data"] = pd.to_datetime(df_cotacoes["data"]).dt.date
df_diario = totais_diarios.rename("valor_total").reset_index()
df_diario["data"] = df_diario["data_transacao"].dt.date
df_consolidado = pd.merge(
    df_diario.drop(columns="data_transacao"),
    df_cotacoes,
    on="data",
    how="left",
)

print("Transações de setembro em SP ou RJ acima de R$ 5.000:")
print(df_setembro)
print("\nSoma do valor por mês e nível de risco:")
print(tabela_risco)
print("\nTransações com Z-Score maior que 2,5:")
print(df_anomalias)
print("\nTotais diários consolidados com as cotações:")
print(df_consolidado)

fig, ax = plt.subplots()
ax.plot(totais_diarios.index, totais_diarios, label="Total diário")
ax.plot(media_movel.index, media_movel, label="Média móvel de 7 dias")
ax.set_ylim(bottom=0)
ax.set_title("Valor total de transações por dia")
ax.set_xlabel("Data")
ax.set_ylabel("Valor (R$)")
ax.legend()
plt.show()