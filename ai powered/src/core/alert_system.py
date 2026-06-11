def generate_alert(
    drop_percentage
):

    if drop_percentage > 50:
        return (
            "🚨 Critical Alert: "
            "Severe Sales Drop"
        )

    elif drop_percentage > 20:
        return (
            "⚠️ Warning: "
            "Sales Drop Detected"
        )

    else:
        return (
            "✅ Stable Sales"
        )