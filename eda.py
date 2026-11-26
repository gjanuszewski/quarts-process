import pandas as pd
import matplotlib.pyplot as plt


def plot_measurement_distributions(df: pd.DataFrame) -> None:
    """Plot distributions of the main measurement variables."""

    columns = [
        "alpha",
        "conductivity_W_mK",
        "temperature",
        "fit quality"
    ]

    labels = [
        "Thermal diffusivity (original units; assumed cm²/s)",
        "Thermal conductivity (W/(m·K))",
        "Measurement temperature (°C)",
        "Fit quality"
    ]

    fig, axes = plt.subplots(2, 2, figsize=(9, 6))

    for ax, column, label in zip(axes.flat, columns, labels):
        ax.hist(df[column].dropna(), bins=40)
        ax.set_xlabel(label)
        ax.set_ylabel("Number of measurements")
        ax.set_title(f"Distribution of {column.replace('_', ' ')}")

    plt.tight_layout()
    plt.show()


def plot_room_temp_conductivity(df: pd.DataFrame) -> None:
    """Plot room-temperature thermal conductivity."""

    room_temp = df.loc[
        (df["temperature"] - 20).abs() <= 0.5
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.hist(
        room_temp["conductivity_W_mK"].dropna(),
        bins=30
    )

    ax.set_xlabel("Thermal conductivity (W/(m·K))")
    ax.set_ylabel("Number of measurements")
    ax.set_title("Room-temperature thermal conductivity")

    plt.tight_layout()
    plt.show()


def summarise_room_temp_repeats(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise repeat room-temperature conductivity measurements."""

    room_temp = df.loc[
        (df["temperature"] - 20).abs() <= 0.5
    ].copy()

    repeat_summary = (
        room_temp
        .groupby("specimen_id")["conductivity_W_mK"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    return repeat_summary


def plot_room_temp_repeat_variability(df: pd.DataFrame) -> None:
    """Plot repeat room-temperature conductivity by specimen."""

    room_temp = df.loc[
        (df["temperature"] - 20).abs() <= 0.5
    ].copy()

    # Put specimens in numerical order
    specimen_order = sorted(
        room_temp["specimen_id"].dropna().unique(),
        key=lambda sample: int(sample.replace("S", ""))
    )

    data = [
        room_temp.loc[
            room_temp["specimen_id"] == specimen,
            "conductivity_W_mK"
        ].dropna()
        for specimen in specimen_order
    ]

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.boxplot(data)

    ax.set_xticks(range(1, len(specimen_order) + 1))
    ax.set_xticklabels(specimen_order)
    ax.set_xlabel("Specimen")
    ax.set_ylabel("Thermal conductivity (W/(m·K))")
    ax.set_title(
        "Repeat variability in room-temperature thermal conductivity"
    )

    plt.tight_layout()
    plt.show()



def plot_conductivity_vs_temperature(df: pd.DataFrame) -> None:
    """Plot mean thermal conductivity against measurement temperature by specimen."""

    temperature_summary = (
        df
        .groupby(["specimen_id", "temperature"])["conductivity_W_mK"]
        .agg(["count", "mean", "std"])
        .reset_index()
    )

    specimen_order = sorted(
        temperature_summary["specimen_id"].dropna().unique(),
        key=lambda sample: int(sample.replace("S", ""))
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    for specimen in specimen_order:
        data = (
            temperature_summary.loc[
                temperature_summary["specimen_id"] == specimen
            ]
            .sort_values("temperature")
        )

        ax.errorbar(
            data["temperature"],
            data["mean"],
            yerr=data["std"],
            marker="o",
            markersize=4,
            capsize=3,
            label=specimen
        )

    ax.set_xlabel("Measurement temperature (°C)")
    ax.set_ylabel("Thermal conductivity (W/(m·K))")
    ax.set_title(
        "Thermal conductivity versus measurement temperature"
    )

    ax.legend(
        title="Specimen",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()

def prepare_eda_measurements(df: pd.DataFrame) -> pd.DataFrame:
    """Remove measurements identified as unsuitable for EDA."""

    eda_measurements = df.loc[
        (df["fit quality"] != 0)
        & ~(
            (df["specimen_id"] == "S12")
            & (df["temperature"] == 295)
        )
    ].copy()

    return eda_measurements


def plot_selected_specimens_vs_temperature(
    df: pd.DataFrame,
    samples: list[str]
) -> None:
    """
    Plot average thermal conductivity against nominal measurement
    temperature for selected specimens.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned measurement data containing calculated conductivity.

    samples : list[str]
        Specimen IDs to include in the plot.
    """
    plot_data = df.loc[
        df["specimen_id"].isin(samples)
    ].copy()

    # Group measurements into nominal 100°C temperature groups
    plot_data["temp_group"] = (
        plot_data["temperature"] / 100
    ).round() * 100

    # Keep the six required temperature groups
    temperature_groups = [0, 100, 200, 300, 400, 500]

    plot_data = plot_data.loc[
        plot_data["temp_group"].isin(temperature_groups)
    ].copy()

    # Display the room-temperature group as 20°C
    plot_data.loc[
        plot_data["temp_group"] == 0,
        "temp_group"
    ] = 20

    # Calculate average conductivity for each specimen and temperature
    plot_summary = (
        plot_data
        .groupby(
            ["specimen_id", "temp_group"],
            as_index=False
        )["conductivity_W_mK"]
        .mean()
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    for specimen in samples:
        specimen_data = (
            plot_summary.loc[
                plot_summary["specimen_id"] == specimen
            ]
            .sort_values("temp_group")
        )

        ax.plot(
            specimen_data["temp_group"],
            specimen_data["conductivity_W_mK"],
            marker="o",
            markersize=5,
            label=specimen
        )

    ax.set_xlabel("Measurement temperature (°C)")
    ax.set_ylabel("Average thermal conductivity (W/(m·K))")
    ax.set_title(
        "Thermal conductivity vs measurement temperature"
    )

    ax.set_xticks([20, 100, 200, 300, 400, 500])
    ax.legend(title="Specimen")

    plt.tight_layout()
    plt.show()


def plot_conductivity_vs_pressure(
    df: pd.DataFrame,
    samples: list[str]
) -> None:
    """
    Plot average room-temperature conductivity against processing
    pressure for selected specimens.

    Each point is labelled with its total porosity.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and merged measurement data.

    samples : list[str]
        Specimen IDs to include in the plot.
    """
    room_temp = df.loc[
        df["specimen_id"].isin(samples)
        & ((df["temperature"] - 20).abs() <= 0.5)
    ].copy()

    # Calculate one row per specimen
    plot_summary = (
        room_temp
        .groupby("specimen_id", as_index=False)
        .agg(
            conductivity_W_mK=("conductivity_W_mK", "mean"),
            pressure_MPa=("Pressure (Mpa)", "first"),
            total_porosity=("Total Pososity (%)", "first")
        )
        .sort_values("pressure_MPa")
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(
        plot_summary["pressure_MPa"],
        plot_summary["conductivity_W_mK"],
        marker="o",
        markersize=10,
        color="red",
        linewidth=3
    )

    # Label each point with its total porosity
    for _, row in plot_summary.iterrows():
        ax.annotate(
            f'{row["total_porosity"]:.1f}%',
            (
                row["pressure_MPa"],
                row["conductivity_W_mK"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )

    ax.set_xlabel("Processing pressure (MPa)")
    ax.set_ylabel("Average thermal conductivity (W/(m·K))")
    ax.set_title("Thermal conductivity vs processing pressure")

    ax.set_xlim(250, 550)
    ax.set_ylim(0.5, 2.5)

    plt.tight_layout()
    plt.show()