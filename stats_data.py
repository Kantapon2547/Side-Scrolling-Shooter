import pandas as pd
import matplotlib.pyplot as plt


class StatisticsManager:
    """Handles recording and reporting game statistics."""

    def __init__(self):
        try:
            self.df = pd.read_csv('data_collection.csv')  # Load CSV on initialization
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = pd.DataFrame()  # Prevent crash

    def analyze_damage(self):
        """Generate a histogram of damage taken during the game."""
        if 'Health Lost' not in self.df.columns:
            print("Column 'Health Lost' not found in CSV.")
            return

        plt.figure(figsize=(8, 6))
        plt.hist(self.df['Health Lost'], bins=10, edgecolor='black', color='skyblue')
        plt.xlabel('Health Lost')
        plt.ylabel('Frequency')
        plt.title('Histogram of Damage Taken')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def analyze_bullets_fired(self):
        """Generate a scatter plot of bullets fired during the game."""
        if 'Bullets Fired' not in self.df.columns:
            print("Column 'Bullets Fired' not found in CSV.")
            return

        plt.figure(figsize=(8, 6))
        plt.scatter(self.df.index, self.df['Bullets Fired'], color='orange', label='Bullets Fired')
        plt.xlabel('Game Instance')
        plt.ylabel('Number of Bullets Fired')
        plt.title('Scatter Plot of Bullets Fired')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def analyze_health_remaining(self):
        """Generate a box plot of health remaining, grouped by level, to analyze difficulty consistency."""
        if 'Health Remaining' not in self.df.columns:
            print("Column 'Health Remaining' not found in CSV.")
            return
        if 'Level' not in self.df.columns:
            print("Column 'Level' not found in CSV.")
            return

        plt.figure(figsize=(10, 6))
        self.df.boxplot(column='Health Remaining', by='Level', grid=True)
        plt.title('Health Remaining by Level')
        plt.suptitle('')  # Remove the automatic 'Boxplot grouped by Level' subtitle
        plt.xlabel('Level')
        plt.ylabel('Health Remaining')
        plt.tight_layout()
        plt.show()

    def analyze_grenade_usage_lineplot(self):
        """Generate a line plot showing grenade usage across different levels."""
        if 'Grenades Thrown' not in self.df.columns or 'Level' not in self.df.columns:
            print("Required columns 'Grenades Thrown' or 'Level' not found in CSV.")
            return

        # Check for missing data
        print(f"Missing values in 'Grenades Thrown': {self.df['Grenades Thrown'].isnull().sum()}")

        # Handle missing data
        self.df = self.df.dropna(subset=['Grenades Thrown'])

        # Ensure 'Grenades Thrown' is numeric
        self.df['Grenades Thrown'] = pd.to_numeric(self.df['Grenades Thrown'], errors='coerce')

        # Group by Level and sum grenade usage
        grenade_usage = self.df.groupby('Level')['Grenades Thrown'].sum().reset_index()
        print(grenade_usage.head())  # Check the grouped data

        if grenade_usage.empty:
            print("No data available for grenade usage.")
            return

        # Plot line chart
        plt.figure(figsize=(8, 6))
        plt.plot(grenade_usage['Level'], grenade_usage['Grenades Thrown'], marker='o', color='red')
        plt.title('Grenade Usage by Level')
        plt.xlabel('Level')
        plt.ylabel('Total Grenades Thrown')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def show_all_stats(self, back_callback=None):
        """Displays all available statistics graphs."""
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import tkinter as tk
        from tkinter import ttk
        import numpy as np

        if self.df.empty:
            print("No statistics data found to display.")
            return

        def update_plot(choice):
            fig.clf()  # Clear the figure to prepare for a new plot
            ax = fig.add_subplot(111)

            if choice == 'Histogram of Damage Taken':
                if 'Health Lost' in self.df.columns:
                    ax.hist(self.df['Health Lost'].dropna(), bins=10, edgecolor='black', color='skyblue')
                    ax.set_title('Histogram of Damage Taken')
                    ax.set_xlabel('Health Lost')
                    ax.set_ylabel('Frequency')
                else:
                    ax.text(0.5, 0.5, "Column 'Health Lost' not found", ha='center', va='center')

            elif choice == 'Bullets Fired Over Games':
                if 'Bullets Fired' in self.df.columns:
                    ax.scatter(self.df.index, self.df['Bullets Fired'], color='orange')
                    ax.set_title('Scatter Plot of Bullets Fired')
                    ax.set_xlabel('Game Instance')
                    ax.set_ylabel('Bullets Fired')
                else:
                    ax.text(0.5, 0.5, "Column 'Bullets Fired' not found", ha='center', va='center')

            elif choice == 'Health Remaining by Level':
                if 'Current Health' in self.df.columns and 'Level' in self.df.columns:
                    self.df.boxplot(column='Current Health', by='Level', ax=ax, grid=True)
                    ax.set_title('Health Remaining by Level')
                    fig.suptitle('')
                    ax.set_xlabel('Level')
                    ax.set_ylabel('Health Remaining')
                else:
                    ax.text(0.5, 0.5, "Required columns not found", ha='center', va='center')

            elif choice == 'Grenade Usage Lineplot':
                if 'Level' in self.df.columns and 'Grenades Thrown' in self.df.columns:
                    # Check if there are any missing values in the relevant columns
                    grenade_data = self.df[['Level', 'Grenades Thrown']].dropna()

                    # Group by Level and sum grenade usage
                    grenade_usage = grenade_data.groupby('Level')['Grenades Thrown'].sum().reset_index()

                    # Check if grenade_usage contains data
                    if not grenade_usage.empty:
                        ax.plot(grenade_usage['Level'], grenade_usage['Grenades Thrown'], marker='o', color='red')
                        ax.set_title('Grenade Usage by Level')
                        ax.set_xlabel('Level')
                        ax.set_ylabel('Total Grenades Thrown')
                        ax.grid(True)
                    else:
                        ax.text(0.5, 0.5, "No data available for grenade usage", ha='center', va='center')
                else:
                    ax.text(0.5, 0.5, "Required columns not found", ha='center', va='center')

            # elif choice == 'Deaths Per Level Analysis':
            #
            #
            canvas.draw()

        # Setup GUI
        win = tk.Tk()
        win.title("Game Statistics Viewer")
        win.configure(bg='black')

        tk.Label(win, text="Select a statistic to view:", bg='black', fg='white', font=("Arial", 14, "bold")).pack(
            pady=10)

        combo = ttk.Combobox(win, values=[
            'Histogram of Damage Taken',
            'Bullets Fired Over Games',
            'Health Remaining by Level',
            'Grenade Usage by Level',
        ])
        combo.pack(pady=5)
        combo.bind("<<ComboboxSelected>>", lambda e: update_plot(combo.get()))

        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack()

        def go_back():
            win.destroy()
            if back_callback:
                back_callback()

        tk.Button(
            win, text="BACK", command=go_back,
            font=("Arial", 16, "bold"),
            bg="gray", fg="white", activebackground="#666", activeforeground="white",
            relief=tk.FLAT, bd=0, padx=40, pady=10
        ).pack(pady=20)

        win.mainloop()
