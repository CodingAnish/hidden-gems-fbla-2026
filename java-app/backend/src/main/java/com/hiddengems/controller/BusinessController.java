package com.hiddengems.controller;

import com.hiddengems.dto.BusinessDto;
import com.hiddengems.service.BusinessService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/businesses")
public class BusinessController {

    private final BusinessService businessService;

    public BusinessController(BusinessService businessService) {
        this.businessService = businessService;
    }

    private Long currentUserId(Authentication auth) {
        if (auth == null || !auth.isAuthenticated() || !(auth.getPrincipal() instanceof Long)) {
            return null;
        }
        return (Long) auth.getPrincipal();
    }

    @GetMapping
    public ResponseEntity<Page<BusinessDto>> list(
            @PageableDefault(size = 20) Pageable pageable,
            Authentication auth
    ) {
        Page<BusinessDto> page = businessService.findAll(pageable, currentUserId(auth));
        return ResponseEntity.ok(page);
    }

    @GetMapping("/{id}")
    public ResponseEntity<BusinessDto> getById(@PathVariable Long id, Authentication auth) {
        Optional<BusinessDto> dto = businessService.findById(id, currentUserId(auth));
        return dto.map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/search")
    public ResponseEntity<Page<BusinessDto>> search(
            @RequestParam String q,
            @PageableDefault(size = 20) Pageable pageable,
            Authentication auth
    ) {
        Page<BusinessDto> page = businessService.searchByName(q, pageable, currentUserId(auth));
        return ResponseEntity.ok(page);
    }

    @GetMapping("/city/{city}")
    public ResponseEntity<Page<BusinessDto>> byCity(
            @PathVariable String city,
            @PageableDefault(size = 20) Pageable pageable,
            Authentication auth
    ) {
        Page<BusinessDto> page = businessService.findByCity(city, pageable, currentUserId(auth));
        return ResponseEntity.ok(page);
    }
}
