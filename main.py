import time
import random
import string
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict
import tracemalloc
import pandas as pd

from array_ import ArrayImpl
from bst import BstImpl
from linked_list import LinkedListImpl
from hash_map import HashMapImpl

# SYNTHETIC DATA GENERATION

class ContactDataGenerator:
    """Generates synthetic contact data for testing"""
    
    @staticmethod
    def generate_random_name() -> str:
        """Generate a random name"""
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", 
                       "James", "Emily", "Robert", "Olivia", "William", "Sophia",
                       "Daniel", "Isabella", "Matthew", "Mia", "Joseph", "Charlotte",
                       "Andrew", "Amelia", "Ryan", "Harper", "Brandon", "Evelyn"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                      "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
                      "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
                      "Martin", "Lee", "Thompson", "White", "Harris", "Clark"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    @staticmethod
    def generate_random_phone() -> str:
        """Generate a random phone number"""
        return f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    @staticmethod
    def generate_random_email(name: str) -> str:
        """Generate a random email based on name"""
        domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "test.com"]
        username = name.lower().replace(" ", ".") + str(random.randint(1, 999))
        return f"{username}@{random.choice(domains)}"
    
    @classmethod
    def generate_contacts(cls, count: int) -> List[Tuple[str, str, str]]:
        """Generate a list of unique contacts"""
        contacts = []
        names_used = set()
        
        while len(contacts) < count:
            name = cls.generate_random_name()
            # Ensure unique names
            if name not in names_used:
                names_used.add(name)
                phone = cls.generate_random_phone()
                email = cls.generate_random_email(name)
                contacts.append((name, phone, email))
        
        return contacts

# PERFORMANCE MEASUREMENT

class PerformanceMeasurement:
    """Measure time and memory performance of operations"""
    
    @staticmethod
    def measure_operation(operation_func, *args, **kwargs) -> Tuple[float, float]:
        # Start memory tracking
        tracemalloc.start()
        
        # Measure execution time
        start_time = time.perf_counter()
        result = operation_func(*args, **kwargs)
        end_time = time.perf_counter()
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        memory_mb = peak / (1024 * 1024)  # Convert to MB
        
        return execution_time_ms, memory_mb, result
    
    @staticmethod
    def measure_multiple_runs(operation_func, runs: int = 5, *args, **kwargs) -> Tuple[float, float]:
        """
        Run operation multiple times and return average time and memory
        """
        times = []
        memories = []
        
        for _ in range(runs):
            exec_time, memory, _ = PerformanceMeasurement.measure_operation(operation_func, *args, **kwargs)
            times.append(exec_time)
            memories.append(memory)
        
        avg_time = sum(times) / len(times)
        avg_memory = sum(memories) / len(memories)
        
        return avg_time, avg_memory

# BENCHMARK TESTS

class ContactManagerBenchmark:
    """Run comprehensive benchmarks on all data structures"""
    
    def __init__(self, dataset_sizes: List[int] = [100, 1000, 10000]):
        self.dataset_sizes = dataset_sizes
        self.results = {
            'Array': {},
            'Linked List': {},
            'Hash Map': {},
            'BST': {}
        }
        self.generator = ContactDataGenerator()
    
    def benchmark_insert(self, manager_class, contacts: List[Tuple[str, str, str]]) -> Tuple[float, float]:
        """Benchmark insertion operation"""
        manager = manager_class()
        
        def insert_all():
            for name, phone, email in contacts:
                manager.insert(name, phone, email)
        
        return PerformanceMeasurement.measure_operation(insert_all)[:2]
    
    def benchmark_search(self, manager, search_names: List[str], runs: int = 100) -> float:
        """Benchmark search operation"""
        total_time = 0
        
        for _ in range(runs):
            name = random.choice(search_names)
            start = time.perf_counter()
            manager.search(name)
            end = time.perf_counter()
            total_time += (end - start) * 1000
        
        return total_time / runs
    
    def benchmark_update(self, manager, update_names: List[str], runs: int = 100) -> float:
        """Benchmark update operation"""
        total_time = 0
        
        for _ in range(runs):
            name = random.choice(update_names)
            new_phone = self.generator.generate_random_phone()
            start = time.perf_counter()
            manager.update(name, phone=new_phone)
            end = time.perf_counter()
            total_time += (end - start) * 1000
        
        return total_time / runs
    
    def benchmark_delete(self, manager, delete_names: List[str]) -> float:
        """Benchmark delete operation"""
        total_time = 0
        count = min(len(delete_names), 100)  # Delete up to 100 contacts
        
        for i in range(count):
            name = delete_names[i]
            start = time.perf_counter()
            manager.delete(name)
            end = time.perf_counter()
            total_time += (end - start) * 1000
        
        return total_time / count
    
    def run_full_benchmark(self):
        """Run complete benchmark suite"""
        implementations = {
            'Array': ArrayImpl,
            'Linked List': LinkedListImpl,
            'Hash Map': HashMapImpl,
            'BST': BstImpl
        }
        
        for size in self.dataset_sizes:
            print(f"\n{'='*60}")
            print(f"Benchmarking with {size} contacts")
            print(f"{'='*60}")
            
            # Generate test data
            contacts = self.generator.generate_contacts(size)
            contact_names = [c[0] for c in contacts]
            
            for impl_name, impl_class in implementations.items():
                print(f"\nTesting {impl_name}...")
                
                # Benchmark Insert
                insert_time, insert_memory = self.benchmark_insert(impl_class, contacts)
                
                # Create manager for other operations
                manager = impl_class()
                for name, phone, email in contacts:
                    manager.insert(name, phone, email)
                
                # Benchmark Search
                search_time = self.benchmark_search(manager, contact_names)
                
                # Benchmark Update
                update_time = self.benchmark_update(manager, contact_names)
                
                # Benchmark Delete
                delete_time = self.benchmark_delete(manager, contact_names)
                
                # Store results
                if size not in self.results[impl_name]:
                    self.results[impl_name][size] = {}
                
                self.results[impl_name][size] = {
                    'insert_time': insert_time,
                    'insert_memory': insert_memory,
                    'search_time': search_time,
                    'update_time': update_time,
                    'delete_time': delete_time
                }
                
                print(f"  Insert: {insert_time:.2f} ms (Memory: {insert_memory:.2f} MB)")
                print(f"  Search: {search_time:.4f} ms (avg per operation)")
                print(f"  Update: {update_time:.4f} ms (avg per operation)")
                print(f"  Delete: {delete_time:.4f} ms (avg per operation)")
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print(f"\n{'='*60}")
        print("PERFORMANCE ANALYSIS REPORT")
        print(f"{'='*60}")
        
        # Theoretical complexity
        print("\n📚 THEORETICAL TIME COMPLEXITY:")
        print("-" * 60)
        complexity_table = pd.DataFrame({
            'Data Structure': ['Array', 'Linked List', 'Hash Map', 'BST (balanced)'],
            'Insert': ['O(n)*', 'O(1)', 'O(1)', 'O(log n)'],
            'Search': ['O(n)', 'O(n)', 'O(1)', 'O(log n)'],
            'Update': ['O(n)', 'O(n)', 'O(1)', 'O(log n)'],
            'Delete': ['O(n)', 'O(n)', 'O(1)', 'O(log n)']
        })
        print(complexity_table.to_string(index=False))
        print("* Array insert is O(n) due to duplicate check")
        
        # Empirical results
        print("\n📊 EMPIRICAL RESULTS:")
        print("-" * 60)
        for size in self.dataset_sizes:
            print(f"\nDataset Size: {size} contacts")
            for impl_name in self.results:
                if size in self.results[impl_name]:
                    data = self.results[impl_name][size]
                    print(f"\n{impl_name}:")
                    print(f"  Insert (total): {data['insert_time']:.2f} ms")
                    print(f"  Search (avg):   {data['search_time']:.4f} ms")
                    print(f"  Update (avg):   {data['update_time']:.4f} ms")
                    print(f"  Delete (avg):   {data['delete_time']:.4f} ms")
                    print(f"  Memory:         {data['insert_memory']:.2f} MB")
    
    def visualize_results(self):
        """Create visualization graphs"""
        sns.set_style("whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Contact Manager Performance Comparison', fontsize=16, fontweight='bold')
        
        operations = ['insert_time', 'search_time', 'update_time', 'delete_time']
        operation_titles = ['Insert Operation', 'Search Operation', 'Update Operation', 'Delete Operation']
        
        for idx, (op, title) in enumerate(zip(operations, operation_titles)):
            ax = axes[idx // 2, idx % 2]
            
            for impl_name in self.results:
                sizes = []
                times = []
                for size in sorted(self.results[impl_name].keys()):
                    sizes.append(size)
                    times.append(self.results[impl_name][size][op])
                
                ax.plot(sizes, times, marker='o', label=impl_name, linewidth=2, markersize=8)
            
            ax.set_xlabel('Dataset Size (number of contacts)', fontsize=11)
            ax.set_ylabel('Time (ms)', fontsize=11)
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Use log scale for better visualization if needed
            if max(times) / min([t for t in times if t > 0] + [1]) > 100:
                ax.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('contact_manager_performance.png', dpi=300, bbox_inches='tight')
        print("\n📈 Performance graphs saved as 'contact_manager_performance.png'")
        plt.show()
        
        # Memory comparison
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for impl_name in self.results:
            sizes = []
            memories = []
            for size in sorted(self.results[impl_name].keys()):
                sizes.append(size)
                memories.append(self.results[impl_name][size]['insert_memory'])
            
            ax.plot(sizes, memories, marker='s', label=impl_name, linewidth=2, markersize=8)
        
        ax.set_xlabel('Dataset Size (number of contacts)', fontsize=12)
        ax.set_ylabel('Memory Usage (MB)', fontsize=12)
        ax.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('contact_manager_memory.png', dpi=300, bbox_inches='tight')
        print("📊 Memory usage graph saved as 'contact_manager_memory.png'")
        plt.show()

def main():
    print("🚀 Contact Manager Performance Analysis")
    print("=" * 60)
    
    # Run benchmarks with different dataset sizes
    benchmark = ContactManagerBenchmark(dataset_sizes=[100, 1000, 10000])
    
    print("\n⏱️  Running benchmarks... This may take a few minutes.")
    benchmark.run_full_benchmark()
    
    print("\n📋 Generating report...")
    benchmark.generate_report()
    
    print("\n📊 Creating visualizations...")
    benchmark.visualize_results()
    
    print("\n✅ Analysis complete!")
    print("\n💡 KEY FINDINGS:")
    print("-" * 60)
    print("• Hash Map: Best for frequent lookups and updates (O(1) operations)")
    print("• BST: Good balance with O(log n) operations and sorted data")
    print("• Linked List: Fast insertions but slow searches")
    print("• Array: Simple but inefficient for large datasets")
    print("\n🎯 RECOMMENDATIONS:")
    print("-" * 60)
    print("• Use Hash Map for real-time contact management systems")
    print("• Use BST when sorted order is important")
    print("• Avoid Array/Linked List for large-scale applications")

if __name__ == "__main__":
    main()