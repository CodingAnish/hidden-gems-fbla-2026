package com.hiddengems.config;

import com.hiddengems.entity.Business;
import com.hiddengems.repository.BusinessRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.List;

@Component
@Profile("!test")
public class DataSeeder implements CommandLineRunner {

    private final BusinessRepository businessRepository;

    public DataSeeder(BusinessRepository businessRepository) {
        this.businessRepository = businessRepository;
    }

    @Override
    public void run(String... args) {
        if (businessRepository.count() > 0) return;
        List<Business> sample = List.of(
                business("Sally Bell's Kitchen", "Restaurants", "102 W Broad St", "Richmond", "VA", "23220", "804-644-2838", "Historic Richmond lunch spot known for box lunches and sweet potato biscuits.", "4.6", 320),
                business("Strawberry Street Cafe", "Cafes", "421 N Strawberry St", "Richmond", "VA", "23220", "804-353-6860", "Eclectic cafe in a converted grocery with bathtub salad bar.", "4.4", 512),
                business("Blackbird Bakery", "Bakeries", "1620 Ownby Ln", "Richmond", "VA", "23220", null, "Artisan breads and pastries.", "4.8", 189),
                business("Mama J's Kitchen", "Soul Food", "415 N 1st St", "Richmond", "VA", "23219", "804-225-7449", "Soul food and Southern comfort in Jackson Ward.", "4.7", 420),
                business("VMFA Museum Shop", "Museums", "200 N Blvd", "Richmond", "VA", "23220", "804-340-1400", "Virginia Museum of Fine Arts museum and cafe.", "4.9", 2100)
        );
        businessRepository.saveAll(sample);
    }

    private static Business business(String name, String category, String address, String city, String state, String zip, String phone, String description, String rating, int reviewCount) {
        Business b = new Business();
        b.setName(name);
        b.setCategory(category);
        b.setAddress(address);
        b.setCity(city);
        b.setState(state);
        b.setZip(zip);
        b.setPhone(phone);
        b.setDescription(description);
        b.setRating(new BigDecimal(rating));
        b.setReviewCount(reviewCount);
        return b;
    }
}
