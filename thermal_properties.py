import pandas as pd


def specific_heat(temp_c):
    """
    Calculate low-quartz specific heat.

    Parameters
    ----------
    temp_c : float or pd.Series
        Measurement temperature in degrees Celsius.

    Returns
    -------
    float or pd.Series
        Specific heat capacity in J/(kg K).
    """
    temp_k = temp_c + 273.15

    cp = (
        0.7310
        + 0.6460e-3 * temp_k
        - 0.1608e5 / temp_k**2
    ) * 1000

    return cp


def bulk_density(th_density, porosity):
    """
    Calculate bulk density from theoretical density and total porosity.

    Parameters
    ----------
    th_density : float
        Theoretical density in kg/m^3.
    porosity : float or pd.Series
        Total porosity as a percentage.

    Returns
    -------
    float or pd.Series
        Bulk density in kg/m^3.
    """
    return th_density * (1 - porosity / 100)


def thermal_conductivity(alpha, density, cp):
    """
    Calculate thermal conductivity.

    Parameters
    ----------
    alpha : float or pd.Series
        Thermal diffusivity in m^2/s.
    density : float or pd.Series
        Bulk density in kg/m^3.
    cp : float or pd.Series
        Specific heat capacity in J/(kg K).

    Returns
    -------
    float or pd.Series
        Thermal conductivity in W/(m K).
    """
    return alpha * density * cp


def calculate_thermal_properties(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate specific heat, density and thermal conductivity.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the calculated thermal properties.
    """
    df = df.copy()

    df["specific_heat"] = specific_heat(
        df["temperature"]
    )

    df["density_kg_m3"] = bulk_density(
        th_density=2650,
        porosity=df["Total Pososity (%)"]
    )

    # Convert thermal diffusivity from cm^2/s to m^2/s
    df["alpha_m2_s"] = df["alpha"] * 1e-4

    df["conductivity_W_mK"] = thermal_conductivity(
        alpha=df["alpha_m2_s"],
        density=df["density_kg_m3"],
        cp=df["specific_heat"]
    )

    return df


def compare_paper_conductivity(
    df: pd.DataFrame,
    paper_values: dict
) -> pd.DataFrame:
    """
    Compare calculated room-temperature conductivity
    with values reported in the paper.
    """

    conductivity_table = (
        df.loc[(df["temperature"] - 20).abs() <= 0.5]
        .groupby("specimen_id", as_index=False)["conductivity_W_mK"]
        .mean()
    )

    conductivity_table["paper_W_mK"] = (
        conductivity_table["specimen_id"].map(paper_values)
    )

    return conductivity_table